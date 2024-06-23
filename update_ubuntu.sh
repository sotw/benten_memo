INSFOLDER=~/.benten_memo
echo "If you are mac user, please use mac port"
echo "http://www.macports.org/"
echo "And download both python and pip"
echo "And don't forget set PATH for ~/bin/sh all wrapped bash script is there"
rm -Rvf $INSFOLDER
rm -vf ~/bin/sh/benten_memo
mkdir -p ~/bin/sh
mkdir -p $INSFOLDER
cp -vf *.py $INSFOLDER
cp -vf benten_memo ~/bin/sh
cp -vf *.db $INSFOLDER

chmod -R 755 $INSFOLDER
chmod -R 755 ~/bin/sh
