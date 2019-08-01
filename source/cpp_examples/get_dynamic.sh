s1="((?<= \t)([^#\n ]*)( *)([^#\n]*))|((?=.)<(.*)>:)"
s2="((?<= \t)([^#\n ]*))"
mkdir dynamic

# For file in /bin/
for f in ./bin/*.b
do
  # Create new filename
  b=$(basename $f)
  f2=${b::${#b}-2}
  f2=$f2"_dynamic.txt"
  echo ./dynamic/$f2

  # Delete this file if it already exists
  rm ./dynamic/$f2

  # Execute file and collect commands
  gdb $f < run.gdb > ./dynamic/$f2

done

./strip_dyn.asm.sh
python strip_library_calls.py
