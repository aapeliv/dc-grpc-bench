ACME_SH_VERSION=2.8.8
wget https://github.com/acmesh-official/acme.sh/archive/${ACME_SH_VERSION}.tar.gz \
       && tar xf ${ACME_SH_VERSION}.tar.gz \
       && mv acme.sh-${ACME_SH_VERSION} ./acme.sh

./acme.sh/acme.sh --issue --standalone -d dgb-tests.coucher.org --keylength ec-256 --fullchain-file fullchain.pem --key-file privkey.pem
