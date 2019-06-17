import os
import re

def main():
  static_dir = "./assembly/"
  dyn_dir = "./dynamic/"
  new_dir = "./dynamic_only_no_library/"
  files = os.listdir(static_dir)
  search_sort = []

  for f in files:
    if "search" in f or "sort" in f:
      if "only" not in f:
        search_sort.append(f)

  for fn in search_sort:
    f = open(static_dir + fn, "r")
    bname = fn.replace("_assembly.txt", "")
    print(bname)
    funcs = find_functions(f)
    f.close()
    dname = bname + "_dynamic.txt"
    fd = open(dyn_dir + dname, "r")
    lines = strip_dyn(fd, funcs)
    fd.close()

    fnew = open(new_dir + bname + "_dynamic_only.txt", 'w+')
    for l in lines:
      fnew.write(l + "\n")
    fnew.close()


def find_functions(f):
  funcs = []
  lines = f.read().splitlines()
  p = re.compile(r"(<.+>:)")
  for l in lines:
    if re.search(p,l):
      funcs.append(l[:-1])
  return funcs


def strip_dyn(f, funcs):
  newlines = []
  lines = f.read().splitlines()
  p = re.compile("(<[^>]+>:)")
  for i in range(len(lines)-1):
    l = lines[i]
    s = re.findall(p,l)
    if len(s) > 0:
      t = s[0]
      plus = t.find("+")
      if plus != -1:
        carot = t.find(">")
        t = t[:plus] + t[carot:-1]

      if t in funcs:
        tb = l.find('\t')
        k = l[tb:]
        if len(k) == 1:
          k = lines[i+1].strip()
        else:
          k = k.strip()
        k = k.split(" ")[0]
        newlines.append(k)

  return newlines


main()
