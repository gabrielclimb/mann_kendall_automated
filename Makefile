lint:
	pre-commit run --all-files

test:
	pytest --cache-clear --cov=src src/tests/

app:
	streamlit run app.py
