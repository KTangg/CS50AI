import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Pages
    pages = corpus.keys()
    # Check for all link in page 
    link_pages = corpus[page]
    link_numb = len(link_pages)
    # Creat Result Dict
    distributions = {}

    if link_numb == 0:
        # No outgoing link
        for page in pages:

            distribution = 1 / len(pages)
            # Add to Dict with {"Page": probability}
            distributions[page] = distribution

        return distributions


    # Distribute with 1 - Damp
    rd_distribution = (1 - damping_factor) / len(pages)
    # Distrubute with Damp
    dp_distribution = damping_factor / link_numb

    # Calculate net Distribute
    for page in pages:
        # In link page then add Damp factor
        if page in link_pages:
            dp_distribution = damping_factor / link_numb
        
        else: 
            dp_distribution = 0
        
        distribution = dp_distribution + rd_distribution
        # Add to Dict with {"Page": probability}
        distributions[page] = distribution
        #print(distributions)

    return distributions
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get Pages
    pages = list(corpus.keys())
    
    # Result dict
    samples = {}
    for page in pages:
        samples[page] = 0

    # Random First Sample & Add to result
    sample_page = random.choice(pages)
    samples[sample_page] = samples[sample_page] + 1

    for i in range(1, n):
        # Generate sample page
        distribution = transition_model(corpus, sample_page, damping_factor)
        sample_page = random.choices(list(pages), weights = distribution.values(), k = 1)[0]
        #print(sample_page)
        # Summing Result
        samples[sample_page] = samples[sample_page] + 1
    #print(samples)
    # Calculate sample distribution
    for sample in samples:
        samples[sample] = samples[sample] / n

    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Get pages
    pages = list(corpus.keys())
    numb_pages = len(pages)
    # Distribution Result
    distributions = {}
    diffs = {}
    distribution = 1 / numb_pages
    for page in pages:
        distributions[page] = distribution
    DIFF = True
    while DIFF:
        temp = {}
        for page in pages:

            # Calculate Second Part of Eq.
            prob_sum = 0

            for key in pages:
                if page in corpus[key]:
                    prob_sum += distributions[key] / len(corpus[key])
                elif len(corpus[key]) == 0:
                    prob_sum += distributions[key] / len(pages)

            # Calculate net Distribution 
            distribution = ((1 - damping_factor) / numb_pages) + (damping_factor * prob_sum)

            # Calculate new diff
            diffs[page] = abs(distributions[page] - distribution)
            #print(f"Diff: {diffs}")
            # Collect new value
            temp[page] = distribution

        #print(f"temp: {temp}")
        #print(f"Distribution: {distributions}")
        # Assign new set of values
        distributions = temp

        cnt = 0
        for diff in diffs:
            if diffs[diff] < 0.001:
                cnt += 1
            
        if cnt == len(diffs):
            DIFF = False

    return distributions


if __name__ == "__main__":
    main()
