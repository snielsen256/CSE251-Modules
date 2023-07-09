"""
Course: CSE 251, week 14
File: functions.py
Author: Stephen Nielsen

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

    My first working DFS took around 68 seconds, which is about the time it 
    would take for 64 families to make 4 batches of concurrent server calls. 
    By making making the husband and wife function calls into their own threads 
    and running them together (in recursive_threads) I cut this time down to 
    just under 8 seconds.


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    # get family JSON
    family_request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    family_request.start()
    family_request.join()


    # create family and add family to tree
    tree.add_family(Family(family_request.get_response()))

    
    # get people JSON
    people_requests = []
    people_requests.append(Request_thread(f'{TOP_API_URL}/person/{family_request.get_response()["husband_id"]}')) # husband
    people_requests.append(Request_thread(f'{TOP_API_URL}/person/{family_request.get_response()["wife_id"]}'))    # wife
    for child_id in family_request.get_response()["children"]: # children
        people_requests.append(Request_thread(f'{TOP_API_URL}/person/{child_id}'))

    for i in people_requests:
        i.start()
    for i in people_requests:
        i.join()

    # create people, add people to tree
    for person_thread in people_requests:
        person_json = person_thread.get_response()
        tree.add_person(Person(person_json))

    
    # make recursive calls --------------------------
    recursive_threads = []

    
    # HUSBAND ---------

    # get husband's id 
    husband_id = family_request.get_response()['husband_id']
    # get husband's parent id
    husband_request = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
    husband_request.start()
    husband_request.join()
    husband_parent_id = husband_request.get_response()['parent_id']
    # make recursive call with husband's parent ID
    if husband_parent_id is not None:
        recursive_threads.append(threading.Thread(target=depth_fs_pedigree, args=(husband_parent_id, tree)))
    
    # end husband -------------


    # WIFE ----------

    # get wife's id 
    wife_id = family_request.get_response()['wife_id']
    # get wife's parent id
    wife_request = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
    wife_request.start()
    wife_request.join()
    wife_parent_id = wife_request.get_response()['parent_id']
    # make recursive call with wife's parent ID
    if wife_parent_id is not None:
        recursive_threads.append(threading.Thread(target=depth_fs_pedigree, args=(wife_parent_id, tree)))

    # end wife ---------------
    
    # do recursive threads
    for rt in recursive_threads:
        rt.start()
    for rt in recursive_threads:
        rt.join()


    


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass