#Imports the mysql.connector module library
import mysql.connector

from flask import Flask, request, jsonify

#app container defined by Flask
app = Flask(__name__)

#attribute to define the route that must exist on the requested URL for the function to be executed.
@app.route('/eval', methods=['GET'])
def square():
    """
    This function evaluates a mathematical expression passed as a query parameter
    and returns the result as a JSON object.
    """
    exp = request.args.get('exp', type=str)
    if exp is None:
        return jsonify({"error": "Please provide an expression to evaluate"}), 400
    return jsonify({"result": eval(exp)})

@app.route('/mr', methods=['GET'])
def memory_recall():
    """
    This function retrieves the value stored in memory and returns it as a JSON object.
    If there is no value stored in memory, it returns None.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM memory")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    memory_value = result[0] if result else None

    return jsonify({"result": memory_value})

@app.route('/mc', methods=['GET'])
def memory_clear():
    """
    This function clears the value stored in memory and returns a JSON object.
    If there is no value stored in memory, it returns None.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM memory")
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"result": "Memory cleared"})

@app.route('/ma', methods=['GET'])
def memory_add():
    """
    This function adds a value to the value stored in memory and returns the updated value as a JSON object.
    If there is no value stored in memory, it initializes memory with the provided value.
    """
    connection = get_connection()
    cursor = connection.cursor()
    insert = False

    try:
        current_value = memory_recall().json['result']

        if current_value is None:
            current_value = 0
            insert = True

        current_value += request.args.get('value', type=float)

        if insert:
            cursor.execute("INSERT INTO memory (value) VALUES (%s)", ([current_value]))
        else:
            cursor.execute("UPDATE memory SET value = %s", ([current_value]))

        connection.commit()

        return jsonify({"result": current_value})
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        connection.close()

@app.route('/mm', methods=['GET'])
def memory_minus():
    """
    This function subtracts a value from the value stored in memory and returns the updated value as a JSON object.
    If there is no value stored in memory, it initializes memory with the negative of the provided value.
    """
    connection = get_connection()
    cursor = connection.cursor()
    insert = False

    try:
        current_value = memory_recall().json['result']

        if current_value is None:
            current_value = 0
            insert = True

        current_value -= request.args.get('value', type=float)

        if insert:
            cursor.execute("INSERT INTO memory (value) VALUES (%s)", ([current_value]))
        else:
            cursor.execute("UPDATE memory SET value = %s", ([current_value]))

        connection.commit()

        return jsonify({"result": current_value})
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        connection.close()


def get_connection():
    """
    This function returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="ebramwell",
        database="calc"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
