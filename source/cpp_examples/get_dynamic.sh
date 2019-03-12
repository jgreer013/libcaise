s1="((?<= \t)([^#\n ]*)( *)([^#\n]*))|((?=.)<(.*)>:)"
s2="((?<= \t)([^#\n ]*))"
for f in ./bin/*.b
do
  b=$(basename $f)
  f2=${b::${#b}-2}
  f2=$f2"_dynamic.txt"
  echo ./dynamic/$f2
  gdb $f -nx < run.gdb > ./dynamic/$f2
  #grep -Po "$s2" > ./assembly/$f2
done
