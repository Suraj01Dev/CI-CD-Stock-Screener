#!/bin/bash
bandit --format json --output bandit-report.json --recursive stock_app
if [[ $? -ne 0 ]]; then
	exit 1
fi

pylint stock_app -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt 
if [[ $? -ne 0 ]]; then
	exit 1
fi

exit 0
