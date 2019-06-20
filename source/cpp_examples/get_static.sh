s1="((?<= \t)([^#\n ]*)( *)([^#\n]*))|((?=.)<(.*)>:)"
s2="((?<= \t)([^#\n ]*))"

# For file in /bin/
for f in ./bin/*
do
  # Create new filenames
  b=$(basename "$f")
  f2=${b::${#b}-2}
  f1=$f2"_assembly.txt"
  # Get objdumps with function tags
  objdump -d $f -j .text | grep -Po "$s1" > ./assembly/$f1
  f2=$f2"_assembly_only.txt"
  # Get objdumps without function tags
  objdump -d $f -j .text | grep -Po "$s2" > ./assembly/$f2
done
