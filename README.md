# physics_equations

App calculating substance distribution.

https://physics-equations.herokuapp.com/

To run locally:

1. go to requirements.txt in the root directory of the project
2. PyCharm will probably ask you to install plugins which will help
3. install everything from requirements.txt
4. go to app.py in the root directory of the project
5. press nice green arrow nex to number of row at the end of file
6. go to http://127.0.0.1:5000

Flask offers live reload. To enable such, add `debug=True` argument to app.run() method, so it would look like
`
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
`
