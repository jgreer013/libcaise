s2="((?<=\t)[a-z]*(?=  ))|(\t\n *\K[a-z]*)"

for f in ./dynamic/*
do
  b=$(basename $f)
  f2=${b::${#b}-4}
  f2=$f2"_only.txt"
  echo ./dynamic_only/$f2
  grep -Po "$s2" $f > ./dynamic_only/$f2
done
