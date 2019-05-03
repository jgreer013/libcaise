s1="((?<= \t)([^#\n ]*)( *)([^#\n]*))|((?=.)<(.*)>:)"
s2="((?<= \t)([^#\n ]*))"
for f in ./bin/*.b
do
  b=$(basename $f)
  f2=${b::${#b}-2}
  f2=$f2"_dynamic_no_library.txt"
  echo ./dynamic_nol/$f2
  rm ./dynamic_nol/$f2
  gdb $f < run_no_library.gdb > ./dynamic_nol/$f2
  #grep -Po "$s2" > ./assembly/$f2
  break
done
