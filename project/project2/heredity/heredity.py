import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    # For Debug
    #print(probabilities)
    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    JOINT = 1
    # Loop through all people
    for person in people:

        # Check for trait and genes
        person_traits = check_person(person, one_gene, two_genes, have_trait)

        if people[person]["father"] and people[person]["mother"]:
            # Check for Father and Mother
            mother_traits = check_person(people[person]["mother"], one_gene, two_genes, have_trait)
            father_traits = check_person(people[person]["father"], one_gene, two_genes, have_trait)
            
            # Chance of having Select trait
            trait_prob = PROBS["trait"][person_traits["gene"]][person_traits["trait"]]

            # Chance of having NO of genes
            gene_prob = parent_prob(person_traits, father_traits, mother_traits)

            # Net person Prob.
            person_prob = trait_prob * gene_prob

        # Use PROBS Table
        else:

            # Chance of having Select trait
            trait_prob = PROBS["trait"][person_traits["gene"]][person_traits["trait"]]

            # Chance of having NO of genes
            gene_prob = PROBS["gene"][person_traits["gene"]]

            # Net person Prob.
            person_prob = trait_prob * gene_prob
            
        JOINT = JOINT * person_prob

    return JOINT

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        person_traits = check_person(person, one_gene, two_genes, have_trait)
        probabilities[person]["gene"][person_traits["gene"]] += p
        probabilities[person]["trait"][person_traits["trait"]] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Loop all person, genes, trait
    for person in probabilities:
        # Gene Part
        total = sum(probabilities[person]["gene"].values())
        #print(total)
        factor = 1 / total

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] * factor
            #print(probabilities[person]["gene"][gene])

        # Trait Part
        total = sum(probabilities[person]["trait"].values())
        factor = 1 / total

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] * factor

def check_person(person, one_gene, two_genes, have_trait):
    """
    Check for person wheter have 0, 1, 2 genes or any trait
    return dict(person: genes(0, 1, 2), trait(True, False))
    """
    # Check for genes
    if person in one_gene:
        gene = 1
    elif person in two_genes:
        gene = 2
    else:
        gene = 0
    
    # Check for trait
    if person in have_trait:
        traits = True
    else:
        traits = False

    return {"gene": gene, "trait": traits}


def parent_prob(person, father_traits, mother_traits):
    """
    Input Person mutated gene to calculate prob of parent passing on mutated gene
    Parent_prob = Passing Mutate gene Prob.
    Not_Parent_prob = Not Passing Mutate gene Prob
    """
    # Mother
    if mother_traits["gene"] == 0:
        mother_prob = PROBS["mutation"]
        not_mother_prob = 1 - PROBS["mutation"]
    elif mother_traits["gene"] == 1:
        mother_prob = (0.5 * PROBS["mutation"]) + (0.5 * (1 - PROBS["mutation"]))
        not_mother_prob = (0.5 * PROBS["mutation"]) + (0.5 * (1 - PROBS["mutation"]))
    else:
        mother_prob = 1 - PROBS["mutation"]
        not_mother_prob = PROBS["mutation"]

    # Father
    if father_traits["gene"] == 0:
        father_prob = PROBS["mutation"]
        not_father_prob = 1 - PROBS["mutation"]
    elif father_traits["gene"] == 1:
        father_prob = (0.5 * PROBS["mutation"]) + (0.5 * (1 - PROBS["mutation"]))
        not_father_prob = (0.5 * PROBS["mutation"]) + (0.5 * (1 - PROBS["mutation"]))
    else:
        father_prob = 1 - PROBS["mutation"]
        not_father_prob = PROBS["mutation"]

    # Calculate child Prob.
    if person["gene"] == 0:
        # (Not Mother) And (Not Father)
        child_prob = not_mother_prob * not_father_prob
    elif person["gene"] == 1:
        # (Not Mother And Father) Or (Mother And Not Father)
        child_prob = (not_mother_prob * father_prob) + (mother_prob * not_father_prob)
    else:
        # Father And Mother
        child_prob = father_prob * mother_prob

    return child_prob

if __name__ == "__main__":
    main()
