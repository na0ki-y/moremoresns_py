PORT = 8080

download_ngrok:
	bash download_ngrok.sh

start_ngrok:
	ngrok http ${PORT} 

init_pip:
	bash init_pip.sh

start:
	uvicorn run:app --reload --port ${PORT}
