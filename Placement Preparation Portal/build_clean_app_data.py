import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DATA_PATH = os.path.join(BASE_DIR, "app_data.py")

with open(APP_DATA_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the circular import
circular_str = "from app import QUESTION_BANKS as EXISTING_QB\n\nQUESTION_BANKS = EXISTING_QB"

base_questions = """
QUESTION_BANKS = {
    "python": {
        "title": "Python Programming Test",
        "questions": [
            {
                "question": "What is the output of the following Python code snippet?",
                "code": "a = [1, 2, 3]\\nb = a\\nb.append(4)\\nprint(len(a))",
                "options": ["3", "4", "Error", "None"],
                "correct_idx": 1,
                "explanation": "In Python, lists are mutable objects and assigned by reference. Both 'a' and 'b' refer to the exact same list in memory, so appending to 'b' modifies 'a'."
            },
            {
                "question": "Which of the following data types in Python is IMMUTABLE?",
                "code": "",
                "options": ["List", "Dictionary", "Tuple", "Set"],
                "correct_idx": 2,
                "explanation": "Tuples, strings, integers, floats, and frozensets are immutable in Python. Lists, dictionaries, and sets are mutable."
            },
            {
                "question": "What is the output of the following list comprehension?",
                "code": "nums = [x**2 for x in range(5) if x % 2 != 0]\\nprint(nums)",
                "options": ["[1, 9]", "[0, 4, 16]", "[1, 3, 5]", "[1, 9, 25]"],
                "correct_idx": 0,
                "explanation": "The odd numbers in range(5) (0, 1, 2, 3, 4) are 1 and 3. Their squares are 1**2 = 1 and 3**2 = 9."
            },
            {
                "question": "What does the Global Interpreter Lock (GIL) in CPython do?",
                "code": "",
                "options": [
                    "Locks memory to prevent unauthorized database access",
                    "Allows only one native thread to execute Python bytecode at a time",
                    "Prevents infinite while loops in scripts",
                    "Enforces strict type declarations"
                ],
                "correct_idx": 1,
                "explanation": "The GIL is a mutex that prevents multiple native OS threads from executing Python bytecode simultaneously in CPython."
            },
            {
                "question": "What is the output of this Python slice operation?",
                "code": "s = 'Placement'\\nprint(s[1:5])",
                "options": ["lace", "lacem", "Plac", "lace "],
                "correct_idx": 0,
                "explanation": "Python slicing is exclusive of the end index. Index 1 to 5 gives 'lace'."
            },
            {
                "question": "What keyword is used to create a generator function in Python?",
                "code": "",
                "options": ["generate", "return", "yield", "async"],
                "correct_idx": 2,
                "explanation": "The 'yield' keyword pauses execution and yields a value back to the caller, creating a generator."
            },
            {
                "question": "What is the output of following dictionary operation?",
                "code": "d = {'a': 1, 'b': 2}\\nprint(d.get('c', 10))",
                "options": ["None", "KeyError", "10", "0"],
                "correct_idx": 2,
                "explanation": "dict.get(key, default) returns the specified default value (10) if the key is not in the dictionary."
            },
            {
                "question": "Which built-in function returns both index and value when iterating over an iterable?",
                "code": "",
                "options": ["zip()", "enumerate()", "map()", "filter()"],
                "correct_idx": 1,
                "explanation": "enumerate() returns pairs of (index, value) during iteration."
            },
            {
                "question": "What will be printed by the following code?",
                "code": "print(type(lambda x: x + 1))",
                "options": ["<class 'function'>", "<class 'lambda'>", "<class 'expression'>", "<class 'int'>"],
                "correct_idx": 0,
                "explanation": "In Python, anonymous functions created with 'lambda' are first-class instances of the function class (<class 'function'>)."
            },
            {
                "question": "How are variable keyword arguments accepted in a Python function definition?",
                "code": "",
                "options": ["*args", "**kwargs", "&kwargs", "...args"],
                "correct_idx": 1,
                "explanation": "**kwargs captures arbitrary keyword arguments as a dictionary inside the function body."
            }
        ]
    },
    "java": {
        "title": "Java Programming Test",
        "questions": [
            {
                "question": "What is the output of comparing two identical String literals with '==' in Java?",
                "code": "String s1 = \\"Hello\\";\\nString s2 = \\"Hello\\";\\nSystem.out.println(s1 == s2);",
                "options": ["true", "false", "Compilation Error", "NullPointerException"],
                "correct_idx": 0,
                "explanation": "String literals are stored in the String Constant Pool in Java. Both point to the exact same pooled reference, so '==' evaluates to true."
            },
            {
                "question": "Which access modifier gives the widest visibility in Java?",
                "code": "",
                "options": ["protected", "default (package-private)", "private", "public"],
                "correct_idx": 3,
                "explanation": "'public' members are accessible from any package, class, or module in the application."
            },
            {
                "question": "Can an abstract class in Java have a constructor?",
                "code": "",
                "options": [
                    "No, abstract classes cannot have constructors",
                    "Yes, called during subclass instantiation via super()",
                    "Only if all methods are static",
                    "Only if the constructor is private"
                ],
                "correct_idx": 1,
                "explanation": "Yes, abstract classes have constructors invoked by subclasses via super() to initialize instance variables."
            },
            {
                "question": "Which of these collections in Java does NOT allow duplicate elements?",
                "code": "",
                "options": ["ArrayList", "Vector", "HashSet", "LinkedList"],
                "correct_idx": 2,
                "explanation": "HashSet implements the Set interface, which guarantees no duplicate elements."
            },
            {
                "question": "What is the default initial capacity of an ArrayList in Java?",
                "code": "",
                "options": ["0 (lazily allocated to 10 on first add)", "16", "32", "50"],
                "correct_idx": 0,
                "explanation": "In modern Java (Java 8+), an empty ArrayList starts with an empty array buffer and resizes to default capacity 10 upon adding the first element."
            },
            {
                "question": "Which keyword is used to prevent method overriding in Java?",
                "code": "",
                "options": ["static", "final", "const", "abstract"],
                "correct_idx": 1,
                "explanation": "Declaring a method as 'final' prevents subclasses from overriding it."
            },
            {
                "question": "What exception is thrown when dividing an integer by zero in Java?",
                "code": "",
                "options": ["NullPointerException", "ArithmeticException", "NumberFormatException", "IllegalArgumentException"],
                "correct_idx": 1,
                "explanation": "Integer division by zero (e.g. 10 / 0) throws java.lang.ArithmeticException: / by zero at runtime."
            },
            {
                "question": "What is the time complexity of get(key) in a well-balanced java.util.HashMap?",
                "code": "",
                "options": ["O(1) average case", "O(N) always", "O(log N) always", "O(N^2)"],
                "correct_idx": 0,
                "explanation": "HashMap provides O(1) constant-time performance on average for get() and put() operations."
            },
            {
                "question": "Which interface must a class implement to enable execution in a separate Thread?",
                "code": "",
                "options": ["Runnable", "Serializable", "Comparable", "Cloneable"],
                "correct_idx": 0,
                "explanation": "Classes implement java.lang.Runnable and its single run() method to execute tasks asynchronously."
            },
            {
                "question": "What is the purpose of the 'finally' block in Java exception handling?",
                "code": "",
                "options": [
                    "Executes only if an exception was caught",
                    "Executes always, regardless of whether an exception occurred or not",
                    "Catches unchecked runtime errors",
                    "Restarts the JVM"
                ],
                "correct_idx": 1,
                "explanation": "The finally block always executes after try and catch blocks, commonly used to release system resources."
            }
        ]
    },
    "cpp": {
        "title": "C++ Programming Test",
        "questions": [
            {
                "question": "What will be printed by this C++ pointer code?",
                "code": "int a = 10;\\nint *p = &a;\\n*p = 25;\\ncout << a;",
                "options": ["10", "25", "Garbage value", "Compilation error"],
                "correct_idx": 1,
                "explanation": "Pointer *p points to the memory address of variable 'a'. Dereferencing *p and assigning 25 directly modifies 'a'."
            },
            {
                "question": "Which keyword is used to dynamically deallocate an object created with 'new' in C++?",
                "code": "",
                "options": ["delete", "free()", "dealloc", "remove"],
                "correct_idx": 0,
                "explanation": "'delete' calls the destructor and deallocates heap memory allocated with 'new'."
            },
            {
                "question": "What is the size of an empty class in C++?",
                "code": "",
                "options": ["0 bytes", "1 byte", "4 bytes", "Compiler error"],
                "correct_idx": 1,
                "explanation": "In C++, an empty class has a size of 1 byte to ensure that two distinct object instances have unique memory addresses."
            },
            {
                "question": "What mechanism enables runtime polymorphism in C++?",
                "code": "",
                "options": ["Templates", "Virtual functions (vtable/vptr)", "Function overloading", "Friend functions"],
                "correct_idx": 1,
                "explanation": "Virtual functions enable late binding (runtime polymorphism) through virtual method tables (vtables)."
            },
            {
                "question": "Which smart pointer in modern C++ implies exclusive ownership of an object?",
                "code": "",
                "options": ["std::shared_ptr", "std::unique_ptr", "std::weak_ptr", "std::auto_ptr"],
                "correct_idx": 1,
                "explanation": "std::unique_ptr cannot be copied, ensuring single exclusive ownership of dynamically allocated heap objects with automatic RAII deletion."
            },
            {
                "question": "What is a dangling pointer?",
                "code": "",
                "options": [
                    "A pointer pointing to NULL",
                    "A pointer pointing to memory that has already been deallocated/freed",
                    "A pointer declared without an asterisk",
                    "A pointer to another pointer"
                ],
                "correct_idx": 1,
                "explanation": "A dangling pointer holds the address of a memory block that has already been freed or destroyed."
            },
            {
                "question": "Which operator cannot be overloaded in C++?",
                "code": "",
                "options": ["+", "==", ":: (Scope resolution operator)", "[]"],
                "correct_idx": 2,
                "explanation": "Operators that cannot be overloaded in C++ include ::, ., .*, and ?:."
            },
            {
                "question": "What does RAII stand for in C++?",
                "code": "",
                "options": [
                    "Resource Acquisition Is Initialization",
                    "Runtime Array Indexing Interface",
                    "Rapid Application Integration Interface",
                    "Recursive Algorithm Implementation Instance"
                ],
                "correct_idx": 0,
                "explanation": "RAII ties resource management (memory, file handles, mutex locks) to the lifespan of stack objects via constructors and destructors."
            },
            {
                "question": "What is the time complexity of std::sort in C++ STL?",
                "code": "",
                "options": ["O(N log N)", "O(N^2)", "O(N)", "O(log N)"],
                "correct_idx": 0,
                "explanation": "std::sort uses Introsort with a guaranteed worst-case and average-case complexity of O(N log N)."
            },
            {
                "question": "What is the difference between a reference and a pointer in C++?",
                "code": "",
                "options": [
                    "A reference must be initialized when created and cannot be null or reseated to another variable",
                    "Pointers cannot be arithmetic",
                    "References allocate 8 bytes on stack",
                    "No difference"
                ],
                "correct_idx": 0,
                "explanation": "References in C++ are aliases that must be initialized upon declaration and cannot be null or reassigned to another object."
            }
        ]
    },
    "dsa": {
        "title": "Data Structures & Algorithms Test",
        "questions": [
            {
                "question": "Which data structure is primarily used to implement Breadth-First Search (BFS) in a Graph?",
                "code": "",
                "options": ["Stack", "Queue", "Priority Queue", "Hash Map"],
                "correct_idx": 1,
                "explanation": "BFS explores nodes level by level in First-In-First-Out order, making a FIFO Queue the ideal data structure."
            },
            {
                "question": "What is the worst-case time complexity of QuickSort?",
                "code": "",
                "options": ["O(N log N)", "O(N)", "O(N^2)", "O(log N)"],
                "correct_idx": 2,
                "explanation": "QuickSort degrades to O(N^2) when the pivot chosen is consistently the smallest or largest element (such as sorted arrays with standard pivot)."
            },
            {
                "question": "How can you detect a cycle in a Singly Linked List in O(1) space?",
                "code": "",
                "options": [
                    "Floyd's Tortoise and Hare (Slow & Fast Pointers)",
                    "Binary Search",
                    "Hash Set of node values",
                    "Dijkstra's Algorithm"
                ],
                "correct_idx": 0,
                "explanation": "Floyd's Cycle-Finding Algorithm uses two pointers moving at speeds 1x and 2x to detect loops in O(N) time and O(1) space."
            },
            {
                "question": "What is the height of a balanced Binary Search Tree (AVL or Red-Black Tree) with N nodes?",
                "code": "",
                "options": ["O(N)", "O(log N)", "O(N^2)", "O(1)"],
                "correct_idx": 1,
                "explanation": "Self-balancing binary trees maintain height bounded by O(log N)."
            },
            {
                "question": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
                "code": "",
                "options": ["Queue", "Stack", "Array", "Linked List"],
                "correct_idx": 1,
                "explanation": "A Stack operates on LIFO order, where elements pushed last are popped first."
            },
            {
                "question": "What is the average time complexity to search an element in a Hash Table?",
                "code": "",
                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                "correct_idx": 0,
                "explanation": "Hash tables compute array bucket indices via hashing functions in O(1) constant time on average."
            },
            {
                "question": "Which sorting algorithm is known to be STABLE?",
                "code": "",
                "options": ["Merge Sort", "QuickSort", "Heap Sort", "Selection Sort"],
                "correct_idx": 0,
                "explanation": "Merge Sort preserves the relative order of elements with equal keys, making it a stable sort."
            },
            {
                "question": "What is the minimum number of queues required to implement a Stack?",
                "code": "",
                "options": ["1", "2", "3", "4"],
                "correct_idx": 1,
                "explanation": "Standard implementation of a Stack using FIFO queues requires 2 queues."
            },
            {
                "question": "In a max-heap of N elements, where is the maximum element stored?",
                "code": "",
                "options": ["At the leaf nodes", "At the root node (index 0)", "At the middle", "Depends on insertion order"],
                "correct_idx": 1,
                "explanation": "In a max-heap, every parent is >= its children, placing the maximum element at the root node."
            },
            {
                "question": "What is the time complexity to find the shortest path using Dijkstra's Algorithm with a Min-Heap?",
                "code": "",
                "options": ["O(V + E)", "O((V + E) log V)", "O(V^3)", "O(E^2)"],
                "correct_idx": 1,
                "explanation": "With an adjacency list and binary priority queue (min-heap), Dijkstra runs in O((V + E) log V) time."
            }
        ]
    },
    "dbms": {
        "title": "DBMS & SQL Queries Test",
        "questions": [
            {
                "question": "Which SQL query correctly retrieves the second highest salary from an Employee table?",
                "code": "",
                "options": [
                    "SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee);",
                    "SELECT salary FROM Employee ORDER BY salary DESC LIMIT 1;",
                    "SELECT SECOND(salary) FROM Employee;",
                    "SELECT salary FROM Employee WHERE rownum = 2;"
                ],
                "correct_idx": 0,
                "explanation": "The subquery finds the maximum salary, and the outer query finds the maximum strictly less than it."
            },
            {
                "question": "What do the letters in the ACID properties of database transactions stand for?",
                "code": "",
                "options": [
                    "Atomicity, Consistency, Isolation, Durability",
                    "Accuracy, Consistency, Integrity, Data",
                    "Access, Control, Index, Dependency",
                    "Algorithm, Cache, Iteration, Deletion"
                ],
                "correct_idx": 0,
                "explanation": "ACID guarantees transactional reliability: Atomicity, Consistency, Isolation, Durability."
            },
            {
                "question": "Which Normal Form removes transitive dependencies?",
                "code": "",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "correct_idx": 2,
                "explanation": "Third Normal Form (3NF) requires a relation to be in 2NF and eliminate transitive functional dependencies between non-key attributes."
            },
            {
                "question": "What is the difference between TRUNCATE and DELETE in SQL?",
                "code": "",
                "options": [
                    "TRUNCATE is DDL, resets table and cannot be rolled back easily; DELETE is DML and row-by-row logged",
                    "DELETE drops the entire table definition; TRUNCATE does not",
                    "They are identical commands with different spelling",
                    "TRUNCATE requires a WHERE clause"
                ],
                "correct_idx": 0,
                "explanation": "TRUNCATE is a fast DDL command deallocating pages; DELETE is DML evaluating WHERE conditions."
            },
            {
                "question": "Which SQL JOIN returns all rows from the left table, and matching rows from the right table?",
                "code": "",
                "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
                "correct_idx": 1,
                "explanation": "LEFT JOIN preserves all records from the left table, filling in NULL for non-matching records from the right table."
            },
            {
                "question": "What data structure is most commonly used for database table indexing?",
                "code": "",
                "options": ["B+ Tree", "Linked List", "Stack", "Binary Search Tree"],
                "correct_idx": 0,
                "explanation": "B+ Trees are the industry standard for database indexes because leaf nodes are linked sequentially for rapid range queries."
            },
            {
                "question": "What is a Foreign Key constraint used for?",
                "code": "",
                "options": [
                    "To ensure Referential Integrity between two related tables",
                    "To speed up network bandwidth",
                    "To encrypt stored passwords",
                    "To allow duplicate primary keys"
                ],
                "correct_idx": 0,
                "explanation": "A Foreign Key establishes a relationship with a Primary Key in another table, guaranteeing referential integrity."
            },
            {
                "question": "Which SQL clause is used to filter groups created by GROUP BY?",
                "code": "",
                "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
                "correct_idx": 1,
                "explanation": "WHERE filters rows before grouping; HAVING filters aggregate results after grouping."
            },
            {
                "question": "How many Clustered Indexes can exist on a single database table?",
                "code": "",
                "options": ["Only 1", "Up to 16", "Unlimited", "0"],
                "correct_idx": 0,
                "explanation": "A Clustered Index dictates the physical ordering of data on disk, so only 1 is permitted per table."
            },
            {
                "question": "What type of lock allows multiple concurrent transactions to read data but prevents modifications?",
                "code": "",
                "options": ["Shared Lock (S-Lock)", "Exclusive Lock (X-Lock)", "Deadlock", "Spinlock"],
                "correct_idx": 0,
                "explanation": "Shared locks allow multiple concurrent reads; Exclusive locks are required for writes."
            }
        ]
    },
    "core_cs": {
        "title": "Core CS, OS & Computer Networks Test",
        "questions": [
            {
                "question": "What are the four necessary conditions for Deadlock to occur in Operating Systems (Coffman Conditions)?",
                "code": "",
                "options": [
                    "Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
                    "Paging, Segmentation, Swapping, Scheduling",
                    "Atomicity, Consistency, Isolation, Durability",
                    "Read, Write, Execute, Terminate"
                ],
                "correct_idx": 0,
                "explanation": "Coffman conditions state that deadlock can only happen if Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait occur concurrently."
            },
            {
                "question": "What layer of the OSI model does the HTTP/HTTPS protocol belong to?",
                "code": "",
                "options": ["Application Layer (Layer 7)", "Transport Layer (Layer 4)", "Network Layer (Layer 3)", "Data Link Layer (Layer 2)"],
                "correct_idx": 0,
                "explanation": "HTTP, HTTPS, FTP, DNS, and SMTP operate at Layer 7: the Application Layer."
            },
            {
                "question": "What happens during the TCP 3-Way Handshake connection establishment?",
                "code": "",
                "options": [
                    "SYN -> SYN-ACK -> ACK",
                    "ACK -> SYN -> FIN",
                    "PING -> PONG -> CONNECT",
                    "HELLO -> ACK -> DATA"
                ],
                "correct_idx": 0,
                "explanation": "Client sends SYN, Server responds with SYN-ACK, Client sends ACK to establish the TCP connection."
            },
            {
                "question": "What is the difference between a Process and a Thread?",
                "code": "",
                "options": [
                    "A process has its own independent address space; threads share the memory address space of their parent process",
                    "Threads cannot execute concurrently",
                    "Processes do not use CPU registers",
                    "A thread is an external hardware device"
                ],
                "correct_idx": 0,
                "explanation": "Processes are isolated with separate virtual memory address spaces. Threads are lightweight units within a process sharing heap, code, and global variables."
            },
            {
                "question": "What is Thrashing in Operating Systems?",
                "code": "",
                "options": [
                    "The OS spending more time swapping pages in and out than executing instructions",
                    "Physical destruction of the hard disk drive",
                    "Instant processor overheating",
                    "Network packet collision"
                ],
                "correct_idx": 0,
                "explanation": "Thrashing occurs when high degree of multiprogramming causes excessive page faults."
            },
            {
                "question": "Which port does HTTPS default to?",
                "code": "",
                "options": ["443", "80", "8080", "22"],
                "correct_idx": 0,
                "explanation": "HTTPS runs over port 443 (encrypted with TLS/SSL). Standard unencrypted HTTP defaults to port 80."
            },
            {
                "question": "What does DNS stand for, and what is its primary role?",
                "code": "",
                "options": [
                    "Domain Name System - translates human-readable domain names into IP addresses",
                    "Dynamic Network Security - encrypts LAN packets",
                    "Digital Number Storage - backs up SQLite databases",
                    "Data Node Server - balances web server loads"
                ],
                "correct_idx": 0,
                "explanation": "DNS translates domain names (like google.com) to machine IP addresses."
            },
            {
                "question": "Which synchronization primitive allows up to 'N' concurrent access permits to a shared resource?",
                "code": "",
                "options": ["Counting Semaphore", "Binary Semaphore / Mutex", "Spinlock", "Condition Variable"],
                "correct_idx": 0,
                "explanation": "A Counting Semaphore maintains an integer count representing available permits, allowing up to N threads access before blocking."
            },
            {
                "question": "Which protocol is connectionless and does not guarantee packet delivery or order?",
                "code": "",
                "options": ["UDP", "TCP", "BGP", "SSH"],
                "correct_idx": 0,
                "explanation": "UDP (User Datagram Protocol) is lightweight, connectionless, and lacks retransmission, making it ideal for live streaming and gaming."
            },
            {
                "question": "What CPU scheduling algorithm assigns a fixed time quantum to each ready process in round-robin fashion?",
                "code": "",
                "options": ["Round Robin (RR)", "First-Come First-Served (FCFS)", "Shortest Job First (SJF)", "Priority Scheduling"],
                "correct_idx": 0,
                "explanation": "Round Robin assigns equal time slices (quanta) cyclically to each process in the queue."
            }
        ]
    },
    "quantitative": {
        "title": "Quantitative Aptitude Test",
        "questions": [
            {
                "question": "A student bought an item for Rs. 500 and sold it for Rs. 650. What is the profit percentage?",
                "code": "",
                "options": ["20%", "25%", "30%", "35%"],
                "correct_idx": 2,
                "explanation": "Profit = Selling Price - Cost Price = 650 - 500 = 150. Profit % = (150 / 500) * 100 = 30%."
            },
            {
                "question": "If A can complete a work in 10 days and B can complete the same work in 15 days, how many days will they take working together?",
                "code": "",
                "options": ["5 days", "6 days", "8 days", "7.5 days"],
                "correct_idx": 1,
                "explanation": "Combined 1 day work = 1/10 + 1/15 = 5/30 = 1/6. Total days = 6 days."
            },
            {
                "question": "A train running at 72 km/hr crosses a pole in 10 seconds. What is the length of the train?",
                "code": "",
                "options": ["150 meters", "200 meters", "250 meters", "300 meters"],
                "correct_idx": 1,
                "explanation": "Speed in m/s = 72 * (5/18) = 20 m/s. Length = 20 m/s * 10 s = 200 meters."
            },
            {
                "question": "The ratio of two numbers is 3:4 and their HCF is 4. What is their LCM?",
                "code": "",
                "options": ["12", "24", "48", "36"],
                "correct_idx": 2,
                "explanation": "Numbers are 12 and 16. LCM(12, 16) = 48."
            },
            {
                "question": "In how many different ways can the letters of the word 'LEADER' be arranged?",
                "code": "",
                "options": ["720", "360", "120", "180"],
                "correct_idx": 1,
                "explanation": "LEADER has 6 letters with 'E' repeating twice. Total permutations = 6! / 2! = 720 / 2 = 360."
            },
            {
                "question": "Two coins are tossed simultaneously. What is the probability of getting at least one head?",
                "code": "",
                "options": ["1/4", "1/2", "3/4", "1"],
                "correct_idx": 2,
                "explanation": "Sample space: {HH, HT, TH, TT}. Outcomes with at least one head: {HH, HT, TH} = 3. Probability = 3/4."
            },
            {
                "question": "What is the simple interest on Rs. 4000 at 5% per annum for 3 years?",
                "code": "",
                "options": ["Rs. 400", "Rs. 600", "Rs. 800", "Rs. 500"],
                "correct_idx": 1,
                "explanation": "SI = (4000 * 5 * 3) / 100 = 600."
            },
            {
                "question": "The average of five numbers is 27. If one number is excluded, the average becomes 25. What is the excluded number?",
                "code": "",
                "options": ["30", "35", "40", "45"],
                "correct_idx": 1,
                "explanation": "Sum of 5 numbers = 135. Sum of remaining 4 numbers = 100. Excluded number = 135 - 100 = 35."
            },
            {
                "question": "Find the compound interest on Rs. 10,000 for 2 years at 10% per annum compounded annually.",
                "code": "",
                "options": ["Rs. 2,000", "Rs. 2,100", "Rs. 2,200", "Rs. 1,900"],
                "correct_idx": 1,
                "explanation": "Amount = 10000 * 1.21 = 12,100. CI = 12,100 - 10,000 = Rs. 2,100."
            },
            {
                "question": "A vendor sells 20 apples for the cost price of 25 apples. Find the profit percentage.",
                "code": "",
                "options": ["20%", "25%", "30%", "15%"],
                "correct_idx": 1,
                "explanation": "Profit% = (5 / 20) * 100 = 25%."
            }
        ]
    },
    "logical": {
        "title": "Logical Reasoning Test",
        "questions": [
            {
                "question": "Find the missing number in the series: 3, 7, 15, 31, 63, ?",
                "code": "",
                "options": ["127", "126", "125", "128"],
                "correct_idx": 0,
                "explanation": "Pattern: Each number is multiplied by 2 and added with 1: (63*2+1 = 127)."
            },
            {
                "question": "Pointing to a photograph, Rohit said, 'She is the daughter of my grandfather's only son.' How is Rohit related to the girl?",
                "code": "",
                "options": ["Brother", "Uncle", "Father", "Cousin"],
                "correct_idx": 0,
                "explanation": "Grandfather's only son is Rohit's father. The daughter of Rohit's father is Rohit's sister, making Rohit her brother."
            },
            {
                "question": "In a certain code, COMPUTER is written as RFUVQNPC. How is MEDICINE written in that code?",
                "code": "",
                "options": ["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "EOJDJEFN"],
                "correct_idx": 0,
                "explanation": "The first and last letters are swapped and reverse shifted with internal letters incremented (+1)."
            },
            {
                "question": "A person walks 10 km North, turns right and walks 10 km, then turns right again and walks 10 km. How far and in what direction is he from the starting point?",
                "code": "",
                "options": ["10 km East", "10 km West", "20 km North", "0 km"],
                "correct_idx": 0,
                "explanation": "He is 10 km East of the starting point."
            },
            {
                "question": "Statements: All cats are dogs. All dogs are birds. Conclusions: (I) All cats are birds. (II) All birds are cats.",
                "code": "",
                "options": ["Only conclusion I follows", "Only conclusion II follows", "Both follow", "Neither follows"],
                "correct_idx": 0,
                "explanation": "Since Cats subset Dogs and Dogs subset Birds, All cats are birds follows."
            },
            {
                "question": "Find the odd one out from the group: 27, 64, 125, 144, 216",
                "code": "",
                "options": ["27", "64", "144", "216"],
                "correct_idx": 2,
                "explanation": "27, 64, 125, and 216 are perfect cubes. 144 is 12^2 (a square, not a cube of an integer)."
            },
            {
                "question": "If '+' means multiply, '-' means divide, '*' means add, and '/' means subtract, calculate: 20 - 5 + 4 * 6 / 2",
                "code": "",
                "options": ["20", "22", "18", "24"],
                "correct_idx": 0,
                "explanation": "20 / 5 * 4 + 6 - 2 = 4 * 4 + 6 - 2 = 16 + 6 - 2 = 20."
            },
            {
                "question": "In a row of 40 students, Priya is 13th from the left end. What is her position from the right end?",
                "code": "",
                "options": ["27th", "28th", "29th", "26th"],
                "correct_idx": 1,
                "explanation": "(40 - 13) + 1 = 28th."
            },
            {
                "question": "Which word cannot be formed using the letters of the word 'RECOMMENDATION'?",
                "code": "",
                "options": ["MEDICINE", "NATION", "MODERN", "COMMON"],
                "correct_idx": 0,
                "explanation": "'MEDICINE' requires two 'I's while RECOMMENDATION has only one 'I'."
            },
            {
                "question": "Today is Monday. What day of the week will it be after 61 days?",
                "code": "",
                "options": ["Tuesday", "Wednesday", "Thursday", "Saturday"],
                "correct_idx": 3,
                "explanation": "61 divided by 7 leaves remainder 5. 5 days after Monday is Saturday."
            }
        ]
    },
    "verbal": {
        "title": "Verbal Ability & English Test",
        "questions": [
            {
                "question": "Choose the word most nearly OPPOSITE in meaning (Antonym) to 'OBSOLETE':",
                "code": "",
                "options": ["Contemporary", "Ancient", "Defunct", "Outdated"],
                "correct_idx": 0,
                "explanation": "Obsolete means outdated. Contemporary means modern and current."
            },
            {
                "question": "Find the correctly spelled word:",
                "code": "",
                "options": ["Accommodate", "Acommodate", "Accomodate", "Acomodate"],
                "correct_idx": 0,
                "explanation": "'Accommodate' has two 'c's and two 'm's."
            },
            {
                "question": "Identify the grammatically correct sentence:",
                "code": "",
                "options": [
                    "Neither of the candidates has submitted their resume.",
                    "Neither of the candidates have submitted his resume.",
                    "Neither of the candidates are submitted.",
                    "Neither candidate have won."
                ],
                "correct_idx": 0,
                "explanation": "'Neither' is a singular indefinite pronoun taking the singular verb 'has'."
            },
            {
                "question": "Choose the synonym for 'CANDID':",
                "code": "",
                "options": ["Frank", "Deceptive", "Shy", "Arrogant"],
                "correct_idx": 0,
                "explanation": "Candid means honest, straightforward, and frank in speech."
            },
            {
                "question": "Fill in the blank: The committee _____ divided in their opinions regarding the budget.",
                "code": "",
                "options": ["was", "were", "is", "has"],
                "correct_idx": 1,
                "explanation": "When collective nouns act as individual members with differing opinions, a plural verb ('were') is used."
            },
            {
                "question": "What is the meaning of the idiom 'To bite the bullet'?",
                "code": "",
                "options": [
                    "To face a difficult situation with courage",
                    "To start a gun fight",
                    "To eat something dangerous",
                    "To quit under pressure"
                ],
                "correct_idx": 0,
                "explanation": "'Bite the bullet' means to bravely endure an unavoidable, difficult situation."
            },
            {
                "question": "Choose the correct preposition: She is proficient _____ Python programming and Data Science.",
                "code": "",
                "options": ["in", "at", "with", "for"],
                "correct_idx": 0,
                "explanation": "The standard English idiom is 'proficient in' a subject or skill."
            },
            {
                "question": "Select the correct one-word substitution for: 'A person who writes computer code or software.'",
                "code": "",
                "options": ["Programmer", "Calligrapher", "Cartographer", "Biographer"],
                "correct_idx": 0,
                "explanation": "A programmer designs and writes computer software code."
            },
            {
                "question": "Choose the word with positive connotation describing someone who handles money carefully:",
                "code": "",
                "options": ["Frugal", "Miserly", "Cheap", "Stingy"],
                "correct_idx": 0,
                "explanation": "Frugal is positive/neutral (wise with money), whereas miserly and stingy carry negative connotations."
            },
            {
                "question": "Identify the passive form: 'The engineer fixed the network bug.'",
                "code": "",
                "options": [
                    "The network bug was fixed by the engineer.",
                    "The network bug is fixed by the engineer.",
                    "The engineer has been fixing the bug.",
                    "The bug had fixed the engineer."
                ],
                "correct_idx": 0,
                "explanation": "Past simple active ('fixed') becomes past simple passive ('was fixed by')."
            }
        ]
    }
}
"""

code = code.replace(circular_str, base_questions.strip())

with open(APP_DATA_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated app_data.py with full independent QUESTION_BANKS!")
