mkdir -p ~/.streamlit/
cp .//.streamlit/config.toml ~/.streamlit/config.toml
echo "\n\
port = $PORT\n\
" >> ~/.streamlit/config.toml