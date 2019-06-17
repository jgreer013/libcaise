s1="((?<= \t)([^#\n ]*)( *)([^#\n]*))|((?=.)<(.*)>:)"
s2="((?<= \t)([^#\n ]*))"
for f in ./bin/*
do
  b=$(basename "$f")
  f2=${b::${#b}-2}
  f1=$f2"_assembly.txt"
  objdump -d $f -j .text | grep -Po "$s1" > ./assembly/$f1
  f2=$f2"_assembly_only.txt"
  objdump -d $f -j .text | grep -Po "$s2" > ./assembly/$f2
done
