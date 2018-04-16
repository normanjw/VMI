from schema_validator import SchemaValidator


SchemaValidator.initialize()

test_1 = {'Jasmine': 'Norman'}

test_2 = {
    "item_ID": "a012",
    "quantity": 26,
    "customer_ID": "b345",
    "date_time": "2018-02-18T09:43Z"
}

test_1_errors = SchemaValidator.validate(test_1)

if test_1_errors:
    print(test_1_errors)
else:
    print("test 1 validated")

test_2_errors = SchemaValidator.validate(test_2)

if test_2_errors:
    print(test_2_errors)
else:
    print("test 2 validated")