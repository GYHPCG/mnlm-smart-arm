
def run(res):
    global result_response
    if res:
        result_response = 1+1
    else:
        result_response = 0
    return result_response

if __name__ == "__main__":
   res = run(0)
   print(res)