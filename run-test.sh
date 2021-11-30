docker-compose up -d 
sleep 2
pipenv run python test-sync-db.py
TEST_STATUS=$?
docker-compose down

if [ $TEST_STATUS -eq 0 ]
then
    echo "Test passed"
else
    echo "Test failed"
fi

exit $TEST_STATUS
