import dbcreds
import mariadb


# I have to connect in different contexts, should make this a function
def connectDB():
    conn = None
    cursor = None

    try:
        conn=mariadb.connect(
                            user=dbcreds.user,
                            password=dbcreds.password,
                            host=dbcreds.host,
                            port=dbcreds.port,
                            database=dbcreds.database
                            )
        cursor = conn.cursor()
    # Only one thing can go wrong, which is the connection to the DB failing
    except:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.close()
        raise ConnectionError("Failed to connect to the database")
    
    return (conn, cursor)

def createPost(username, content):

    # Create the variables so they are visible in the finally scope
    conn = None
    cursor = None
        
    try:
        (conn, cursor) = connectDB()
        cursor.execute("INSERT INTO blog_post(username, content) VALUES(?,?)", [username,content])
        conn.commit()
        print("Post successfully created!\n\n")
    # I know that my own function can raise a ConnectionError, should handle it
    except ConnectionError:
        print("Error while attempting to connect to the database")
    except mariadb.DataError:
        print("Something wrong with your data")
    except mariadb.OperationalError:
        print("Operational error on the connection")
    except mariadb.ProgrammingError:
        print("Your query was wrong")
    except mariadb.IntegrityError:
        print("Your query would have broken the database and we stopped it")
    except:
        print("Something went wrong")
    finally:
        if (cursor != None):
            cursor.close()

        if (conn != None):
            conn.rollback()
            conn.close()


def getAllPosts():
    # Create the variables so they are visible in the finally scope
    conn = None
    cursor = None
        
    try:
        (conn, cursor) = connectDB()
        cursor.execute("SELECT * FROM blog_post")
        posts = cursor.fetchall()
        prettyPrintPosts(posts)
    # I know that my own function can raise a ConnectionError, should handle it
    except ConnectionError:
        print("Error while attempting to connect to the database")
    except mariadb.DataError:
        print("Something wrong with your data")
    except mariadb.OperationalError:
        print("Operational error on the connection")
    except mariadb.ProgrammingError:
        print("Your query was wrong")
    except mariadb.IntegrityError:
        print("Your query would have broken the database and we stopped it")
    except:
        print("Something went wrong")
    finally:
        if (cursor != None):
            cursor.close()

        if (conn != None):
            conn.rollback()
            conn.close()


def prettyPrintPosts(posts):
    # I assume these maximum lengths for the columns of the table, otherwise the padding breaks
    USER_LENGTH=20
    ID_LENGTH=5
    POST_LENGTH=140

    header = "Username".ljust(USER_LENGTH), "Content".ljust(POST_LENGTH), "ID".ljust(ID_LENGTH)
    print(  "|"+
            "|".join(header)+
            "|")
    # Plus 4 for the vertical separation bars
    print("-"*(USER_LENGTH+ID_LENGTH+POST_LENGTH+4))

    # I know that fetchall returns an array of tuples, so I know how to get each individual value (this also assumes I know the order of columns in my DB)
    for post in posts:
        # Pad each part with spaces for consistent display, regardless of data length
        padded_post = (post[0].ljust(USER_LENGTH), post[1].ljust(POST_LENGTH), str(post[2]).ljust(ID_LENGTH))
        print(  "|"+
                "|".join(padded_post)+
                "|")
        print("-"*(USER_LENGTH+ID_LENGTH+POST_LENGTH+4))



print("Hello and welcome to the blog!")

while (True):

    print("\n\nPlease select one of the following options:\n"+
        "1: Write a new post\n"+
        "2: View all existing posts\n"+
        "3: Exit")

    choice = input("Choice: ")

    # Define the valid choices and raise an exception if choice is invalid
    if (choice not in ["1","2","3"]):
        raise ValueError("Error! Invalid choice, exiting")



    if (choice == "1"):

        print("Please enter your username:", end="")
        username = input()

        if (username == ""):
            raise ValueError("Error! Post cannot be empty, exiting")

        print("Please enter your post:")
        content = input()

        if (content == ""):
            raise ValueError("Error! Post cannot be empty, exiting")

        createPost(username, content)

    elif(choice == "2"):
        print("Fetching all posts...\n\n")
        posts = getAllPosts()

    elif(choice == "3"):
        exit()
