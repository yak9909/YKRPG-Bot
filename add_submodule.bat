git submodule add https://github.com/Rapptz/discord.py discord
cd discord
git config core.sparsecheckout true
echo discord/ > ../.git/modules/discord/info/sparse-checkout
echo ../ >> ../.git/modules/discord/info/sparse-checkout
git read-tree -mu HEAD
cd ..

git submodule add https://github.com/yak9909/ykutils modules/ykutils
cd modules/ykutils
git config core.sparsecheckout true
echo ykutils/ > ../../.git/modules/modules/ykutils/info/sparse-checkout
echo ../ >> ../../.git/modules/modules/ykutils/info/sparse-checkout
git read-tree -mu HEAD
cd ../..