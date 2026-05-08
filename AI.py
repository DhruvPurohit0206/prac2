# AI-1
from collections import deque 
 
# Undirected graph 
graph = { 
    'A': ['B', 'C'], 
    'B': ['A', 'D', 'E'], 
    'C': ['A', 'E'], 
    'D': ['B'], 
    'E': ['B', 'C'] 
} 
 
# DFS (Recursive) 
def dfs(graph, node, visited=None): 
    if visited is None: 
        visited = set() 
 
    visited.add(node) 
    print(node, end=" ") 
 
    for neighbor in graph[node]: 
        if neighbor not in visited: 
            dfs(graph, neighbor, visited) 
 
# BFS (Queue) 
def bfs(graph, start): 
    visited = set([start]) 
    queue = deque([start]) 
 
    while queue: 
        node = queue.popleft() 
        print(node, end=" ") 
 
        for neighbor in graph[node]: 
            if neighbor not in visited: 
                visited.add(neighbor) 
                queue.append(neighbor) 
 
print("DFS Traversal:") 
dfs(graph, 'A') 
print("\n")  
print("\nBFS Traversal:") 
bfs(graph, 'A') 

# AI-2
import heapq 
 
def a_star(grid, start, end): 
    open_list = [] 
    heapq.heappush(open_list, (0, start)) 
 
    came_from = {} 
    g_cost = {start: 0} 
 
    while open_list: 
        current = heapq.heappop(open_list)[1] 
 
        if current == end: 
            path = [] 
            while current in came_from: 
                path.append(current) 
                current = came_from[current] 
            path.append(start) 
            return path[::-1] 
 
        x, y = current 
 
        for move in [(0,1), (1,0), (0,-1), (-1,0)]: 
            neighbor = (x + move[0], y + move[1]) 
 
            if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])): 
                continue 
 
            if grid[neighbor[0]][neighbor[1]] == 1: 
                continue 
 
            new_g = g_cost[current] + 1 
 
            if neighbor not in g_cost or new_g < g_cost[neighbor]: 
                g_cost[neighbor] = new_g 
 
                f = new_g + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1]) 
 
                heapq.heappush(open_list, (f, neighbor)) 
                came_from[neighbor] = current 
 
    return None 
 
grid = [ 
    [0,0,0], 
[1,1,0], 
[0,0,0] 
] 
start = (0,0) 
end = (2,2) 
print(a_star(grid, start, end))


# AI-2
class Job: 
    def __init__(self, id, deadline, profit): 
        self.id = id 
        self.deadline = deadline 
        self.profit = profit 
 
def job_scheduling(jobs): 
    # Sort jobs by profit (Greedy) 
    jobs.sort(key=lambda x: x.profit, reverse=True) 
 
    # Find max deadline 
    max_deadline = max(job.deadline for job in jobs) 
 
    # Create slots 
    slots = ['-'] * max_deadline 
    total_profit = 0 
 
    # Assign jobs 
    for job in jobs: 
        for i in range(job.deadline - 1, -1, -1): 
            if slots[i] == '-': 
                slots[i] = job.id 
                total_profit += job.profit 
                break 
 
    return slots, total_profit 
 
# Input 
jobs = [ 
    Job("j1", 2, 15), 
    Job("j2", 3, 27), 
    Job("j3", 3, 10), 
    Job("j4", 3, 100), 
    Job("j5", 4, 150) 
] 
 
# Call function 
result, profit = job_scheduling(jobs) 
 
# Output 
print("Scheduled Jobs:", result) 
print("Total Profit:", profit)


# AI-4
def is_safe(board, row, col, n): 
    # Check same column 
    for i in range(row): 
        if board[i][col] == 1: 
            return False 
 
    # Check left diagonal 
    i, j = row-1, col-1 
    while i >= 0 and j >= 0: 
        if board[i][j] == 1: 
            return False 
        i -= 1 
        j -= 1 
 
    # Check right diagonal 
    i, j = row-1, col+1 
    while i >= 0 and j < n: 
        if board[i][j] == 1: 
            return False 
        i -= 1 
        j += 1 
 
    return True 
 
def solve_n_queens(board, row, n): 
    if row == n: 
        return True 
 
    for col in range(n): 
        if is_safe(board, row, col, n): 
            board[row][col] = 1 
 
            if solve_n_queens(board, row+1, n): 
                return True 
 
            # Backtrack 
            board[row][col] = 0 
 
    return False 
 
# MAIN 
n = int(input("Enter number of queens: ")) 
 
board = [[0]*n for _ in range(n)] 
 
if solve_n_queens(board, 0, n): 
    print("\nSolution:") 
    for row in board: 
        print(row) 
else: 
    print("No solution exists")



# AI-5
import re 
 
# Valid cities (you can add more) 
valid_cities = ["pune", "mumbai", "delhi", "bangalore", "chennai", "hyderabad"] 
 
# Context memory 
context = { 
    "booking": False, 
    "source": "", 
    "destination": "", 
    "date": "" 
} 
 
def chatbot_response(user_input): 
    user_input = user_input.lower().strip() 
 
    # BOOKING FLOW (Context Based) 
    if context["booking"]: 
 
        # Step 1: Source 
        if context["source"] == "": 
            if user_input in valid_cities: 
                context["source"] = user_input 
                return "Great! Where do you want to travel to?" 
            else: 
                return f"Please enter a valid city ({', '.join(valid_cities)})" 
 
        # Step 2: Destination 
        elif context["destination"] == "": 
            if user_input in valid_cities: 
                context["destination"] = user_input 
                return "Enter travel date (DD-MM-YYYY):" 
            else: 
                return f"Please enter a valid destination ({', '.join(valid_cities)})" 
 
        # Step 3: Date 
        elif context["date"] == "": 
            if re.match(r"\d{2}-\d{2}-\d{4}", user_input): 
                context["date"] = user_input 
                context["booking"] = False 
 
                return (f"Searching buses from {context['source'].title()} " 
                        f"to {context['destination'].title()} on {context['date']}...\n" 
                        "Found 5 buses. Prices start from ₹500.\n" 
                        "Do you want to proceed with booking? (yes/no)") 
            else: 
                return "Invalid date format. Please use DD-MM-YYYY." 
 
    # NORMAL RESPONSES 
    responses = { 
        r"\b(hello|hi|hey)\b": "Hello! Welcome to RedBus Chatbot. How can I help you?", 
        r"\b(book ticket|bus booking|book bus)\b": "Sure! Where are you traveling from?", 
        r"\b(cancel ticket|cancellation)\b": "You can cancel tickets from 'My Bookings'.", 
        r"\b(refund)\b": "Refunds are processed within 5-7 working days.", 
        r"\b(offers|discount)\b": "Use code BUS10 to get 10% discount!", 
        r"\b(payment)\b": "We support UPI, cards, net banking, and wallets.", 
        r"\b(track|location)\b": "Live tracking starts 1 hour before departure.", 
        r"\b(luggage)\b": "You can carry up to 15kg luggage.", 
        r"\b(help|support)\b": "Call 1800-123-1234 for customer support." 
    } 
 
    #  Activate booking 
    if re.search(r"\b(book ticket|bus booking|book bus)\b", user_input): 
        context["booking"] = True 
        context["source"] = "" 
        context["destination"] = "" 
        context["date"] = "" 
        return "Sure! Where are you traveling from?" 
 
    #  Pattern match 
    for pattern, response in responses.items(): 
        if re.search(pattern, user_input): 
            return response 
 
    return "Sorry, I didn't understand. Try asking about booking, refund, or offers." 
 
#  CHAT LOOP 
print("=== RedBus Smart Chatbot ===") 
print("Type 'bye' to exit.\n") 
 
while True: 
    user = input("You: ") 
 
    if user.lower() in ["bye", "exit"]: 
        print("Chatbot: Goodbye! Safe travels!") 
        break 
 
    reply = chatbot_response(user) 
    print("Chatbot:", reply)



# AI-6
# Expert System: Employee Performance Evaluation (Forward Chaining) 
 
# Knowledge Base (Rules) 
rules = { 
    "Outstanding": { 
        "conditions": ["high_task", "high_problem", "high_team"], 
        "message": "Eligible for promotion and leadership roles." 
    }, 
    "Good": { 
        "conditions": ["medium_task", "medium_problem"], 
        "message": "Consistent performance. Minor improvements needed." 
    }, 
    "Average": { 
        "conditions": ["low_task", "low_problem"], 
        "message": "Needs improvement and training." 
    }, 
    "Poor": { 
        "conditions": ["very_low_task", "very_low_problem"], 
        "message": "Immediate action required. Performance review needed." 
    } 
} 
 
#  Convert score to facts 
def generate_facts(scores): 
    facts = [] 
 
    if scores["task"] >= 4: 
        facts.append("high_task") 
    elif scores["task"] >= 3: 
        facts.append("medium_task") 
    elif scores["task"] >= 2: 
        facts.append("low_task") 
    else: 
        facts.append("very_low_task") 
 
    if scores["problem"] >= 4: 
        facts.append("high_problem") 
    elif scores["problem"] >= 3: 
        facts.append("medium_problem") 
    elif scores["problem"] >= 2: 
        facts.append("low_problem") 
    else: 
        facts.append("very_low_problem") 
 
    if scores["team"] >= 4: 
        facts.append("high_team") 
 
    return facts 
 
#  Inference Engine (Forward Chaining) 
def forward_chain(facts): 
    for category, data in rules.items(): 
        if all(cond in facts for cond in data["conditions"]): 
            return category, data["message"] 
 
    return "Uncertain", "Insufficient data for evaluation." 
 
#  Input Validation 
def get_rating(msg): 
    while True: 
        try: 
            val = int(input(msg)) 
            if 1 <= val <= 5: 
                return val 
            else: 
                print("Enter value between 1 and 5") 
        except: 
            print("Invalid input") 
 
#  Main System 
def expert_system(): 
    print("\n=== Expert System: Employee Performance Evaluation ===\n") 
 
    name = input("Enter Employee Name: ") 
    role = input("Enter Role/Department: ") 
 
    print("\nRate (1-5):") 
 
    scores = { 
        "team": get_rating("Teamwork: "), 
        "task": get_rating("Task Completion: "), 
        "problem": get_rating("Problem Solving: ") 
    } 
 
    # Generate facts 
    facts = generate_facts(scores) 
 
    # Apply inference 
    result, message = forward_chain(facts) 
 
    
# Output 
print("\n--- Evaluation Report ---") 
print(f"Name: {name}") 
print(f"Role: {role}") 
print(f"Facts Derived: {facts}") 
print(f"Performance: {result}") 
print(f"Recommendation: {message}") 
# Run 
expert_system()

