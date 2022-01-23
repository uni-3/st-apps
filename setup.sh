mkdir -p ~/.streamlit/
cp ./sake-gaikyo/.streamlit/config.toml ~/.streamlit/config.toml
echo "\
port = $PORT\n\
" >> ~/.streamlit/config.toml