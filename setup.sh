mkdir -p ~/.streamlit/
cp ./sake-gaikyo/.streamlit/config.toml ~/.streamlit/config.toml
echo "\n\
port = $PORT\n\
" >> ~/.streamlit/config.toml