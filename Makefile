export PYTHONASYNCIODEBUG=1
export PYTHONWARNINGS=default

test:
	# python -m unittest
	nosetests -v

pylint:
	pylint -f parseable websocket_redis/ --rcfile .pylint

coverage:
	python -m coverage erase
	python -m coverage run --branch --source=websocket_redis -m unittest
	python -m coverage html

install:
	python setup.py install

publish-test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

publish:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage build compliance/reports dist docs/_build htmlcov MANIFEST nosetests.xml websocket_redis.egg-info .tox