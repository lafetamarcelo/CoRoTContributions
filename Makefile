
docs:
	make html_note


html_update:
	cp -r ./temp/_build/html/ ./docs/

html_note:
	rm -r ./docs/*.ipynb
	cp 01\ -\ Reading\ and\ Plotting.ipynb ./docs
	cp 02\ -\ Building\ and\ creating\ features.ipynb ./docs
	cp 03\ -\ Machine\ Learning\ -\ XGBoost\ Classifier.ipynb ./docs
	cp 03\ -\ Machine\ Learning\ -\ Decision\ Trees.ipynb ./docs

clean_doc:
	rm -r ./docs
	mkdir -p docs