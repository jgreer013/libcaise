import os


def get_top_topics(n, dir, fn):
    file_name = dir + fn
    doc_top_topics = {}
    with open(file_name, 'r') as f:
        for line in f:
            topics = {}
            line = line.strip().split(" ")
            if len(line) > 1:
                doc = line[0]
                for pair in line[2:]:
                    topic, weight = pair.split(":")
                    weight = int(weight)
                    topics[topic] = weight
                doc_top_topics[doc] = [(top, topics[top]) for top in sorted(topics.keys(), key=lambda x: topics[x], reverse=True)[:n]]
    return doc_top_topics

def get_top_terms(n, dir, fn):
    file_name = dir + fn
    topic_top_terms = {}
    topic_terms = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().split(" ")
            if len(line) > 1:
                term = line[0]
                for pair in line[2:]:
                    topic, weight = pair.split(":")
                    weight = int(weight)
                    if topic not in topic_terms:
                        topic_terms[topic] = []
                    topic_terms[topic].append((term, weight))

    for topic in topic_terms:
        terms = topic_terms[topic]
        terms = sorted(terms, key=lambda x: x[1], reverse=True)[:n]
        topic_top_terms[topic] = terms

    return topic_top_terms

def get_term_dict(dir, fn):
    file_name = dir + fn
    term_dict = {}
    clus = get_clusters()
    t = 1
    with open(file_name,'r') as f:
        for line in f:
            term = line.strip()
            cids = term.split("_")
            for i in range(len(cids)):
                cid = cids[i]
                if len(clus[cid]) == 1:
                    cids[i] = clus[cid][0]


            term_dict[str(t)] = "_".join(cids)
            t += 1


    return term_dict

def get_doc_names(dir):
    files = os.listdir(dir)
    doc_names = []
    for f in files:
        if f[-8:] == "only.txt":
            doc_names.append(f)
    return doc_names

def get_clusters():
    fn = "clusters_full.txt"
    clus = {}
    with open(fn, 'r') as f:
        for line in f:
            term, cid = line.strip().split(",")
            if cid not in clus:
                clus[cid] = []
            clus[cid].append(term)
    return clus

def print_tops(doc, top_topics, top_terms, term_dict, doc_names, pterms=True):
    doc_top = top_topics[str(doc)]
    print(doc_names[int(doc)], "Top Topics:", doc_top)
    if pterms:
        for top in doc_top:
            t = top[0]
            print(t, [(term_dict[x[0]], x[1]) for x in top_terms[t]])
    print()


n, m = 5, 3
dir = "./data/LightLDA/assembly8_low_ab_2/"
fn_top = "doc_topic.0"
fn_term = "server_0_table_0.model"
fn_dict = "vocab.assembly8.txt"
tops = get_top_topics(n, dir, fn_top)
terms = get_top_terms(m, dir, fn_term)
term_dict = get_term_dict(dir, fn_dict)
docnames = get_doc_names("./source/cpp_examples/assembly/")

search_sort = []
for i in range(len(docnames)):
    fn = docnames[i]
    if "search" in fn or "sort" in fn:
        search_sort.append(i)

for i in sorted(search_sort, key=lambda x: "sort" in docnames[x]):
    print_tops(i, tops, terms, term_dict, docnames, pterms=1)

"""
bins = [[] for i in range(len(terms))]
for i in range(len(docnames)):
    top_topics = tops[str(i)]
    bins[int(top_topics[0][0])].append(docnames[i])


for b in range(len(bins)):
    print(b)
    for f in bins[b]:
        print(f)
    print()
"""
