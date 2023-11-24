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

    links = list()  
    PR_dist = dict()    
    # list the links for page
    for filename in corpus:
      if filename in page:
        links = set(corpus[filename])
    PR =0 
    # initialize dictionary
    for filename in corpus:
      if filename in links and links != set():
        PR = damping_factor*1/len(links) + (1-damping_factor)*1/len(corpus)
        PR_dist[filename] = PR
      elif filename not in links and links != set():
        PR = (1-damping_factor)*1/len(corpus)
        PR_dist[filename] = PR
      elif links == set():
        PR = 1/len(corpus)
        PR_dist[filename] = PR
    return PR_dist
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    i = 0
    PR_dist = PRcount = dict()
    samples = []
    # initialize dictionaries
    for filename in corpus:
      PR_dist[filename] = 0
      PRcount[filename] = 0
    
    random_page = random.choice(list(corpus.keys()))
    samples.append(random_page)
    
    for i in range (1,n):
      
      PR_dist = transition_model(corpus, random_page, damping_factor)
      random_page = random.choices(list(PR_dist.keys()), weights = list(PR_dist.values()), k=1)
      samples.append(random_page[0])
      
  # normalize
    
    for file in PRcount:
      PRcount[file] = samples.count(file)/len(samples)

    return PRcount


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
  """
    PR =0
    i=0
    iteration = 1
    PR_dist = dict()
    out_link = dict()
    PRold = dict()
    olinks = dict()
    enlace = set()
  
    # initialize dictionary
    for filename in corpus:
      PR_dist[filename] = 1/len(corpus)
      PRold[filename] = 1/len(corpus)
      out_lk = 0
      
      # initialize outlet links dict.
      enlace = set()
      for file in corpus:
        if filename in corpus[file]: 
          out_lk += 1
          enlace.add(file)
      olinks[filename] = enlace
      out_link[filename] = out_lk
    

    'print(corpus, olinks)'
      
      
    while i < len (corpus):
      i= 0
      for filename in PR_dist:
        
        if corpus[filename] == set():
          PR = 1/(len(corpus))
        else:   
          PR = (1-damping_factor)/len(corpus)
          'print(PR)'
          for links in olinks[filename]:
            PR += damping_factor*PRold[links]/len(corpus[links]) 
            'print("filename", filename, "links", links, "num links", len(corpus[links]), "PRi" , PR_dist[links])'
          PR_dist[filename] = PR
          'print(PR_dist[filename])'
          
        iteration = abs(PR_dist[filename]-PRold[filename])
        if iteration < 0.001:
          i += 1
     
      PRold = PR_dist.copy()
    return PR_dist


if __name__ == "__main__":
    main()
