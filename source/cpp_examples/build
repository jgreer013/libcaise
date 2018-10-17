for f in */*.cpp
do
  b=$(basename "$f")
  f2=${b::${#b}-4}
  g++ -o bin/$f2.b $f
done
