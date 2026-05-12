.PHONY: test install-dev clean

test:
	python3 -m pytest

install-dev:
	python3 -m pip install -e ".[dev]"

clean:
	rm -rf .pytest_cache dist build *.egg-info __pycache__ codewiki/__pycache__ tests/__pycache__
