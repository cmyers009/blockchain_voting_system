from voteInfo import voteInfo

#checks if the vote cast was valid
def valid_vote(vote):
    #if vote.casefold() == 'cpe' or vote.casefold() == 'ece':
    if vote == 'cpe' or vote == 'ece':
        return True
    else:
        return False

#Gets vote info from cli inputs and returns voteInfo object
def get_vote():
    name = input("Enter your name: ")

    vote = input("Enter your vote (ECE/CPE): ")
    while(valid_vote(vote) == False):
        print("You may only vote for 'ece' or 'cpe'")
        vote = input("Enter your vote (ECE/CPE): ")

    email = input("Enter your email: ")

    #confirming input and adding to queue
    print("\nname: " + name + "   vote: " + vote + "   email: " + email)
    #confirm = input("Confirm this information is correct and you would like to submit your vote (Y/N)")

    #if confirm.casefold() == "Y".casefold():
    return voteInfo(vote,name,email)
    #else:
    #    return None
    #    print("Submission Canceled")