
MULTIPLIER_MARKERS = ["", "D", "T"]

def __get_double_finishes():
    return [(f"{x}x2", x*2) for x in range(1,20+1)]


def __add_follow_ups(remaining, darts, str_representation, amount, results):
    follow_ups = get_checkouts_for_with_darts(remaining - amount, darts-1)
    #print(f"Looking for single follow ups: {follow_ups}")
    if len(follow_ups) != 0:
        for follow_up in follow_ups:
            follow_up.append((str_representation, amount))
        results.extend(follow_ups)

def get_checkouts_for_with_darts(remaining, darts = 3):
    if remaining <= 0 or darts == 0:
        return []
    
    #if darts == 1:
    
        
     #   return []
    
    results = []
    for i in range(1,20+1):
        # Singles, doubles, triples
        for multiplier in [1,2,3]:
            if i * multiplier < remaining:
                #__add_follow_ups(remaining, darts, f"{i}x{multiplier}", i*multiplier, results)
                __add_follow_ups(remaining, darts, f"{MULTIPLIER_MARKERS[multiplier-1]}{i}", i*multiplier, results)
    
    __add_follow_ups(remaining, darts, "25", 25, results)
    __add_follow_ups(remaining, darts, "BULL", 50, results)
    
    
    if remaining == 50:
        results.append([("BULL", 50)])
    if remaining <= 40 and remaining > 0 and remaining % 2 == 0:
        results.append([(f"D{remaining//2}", remaining)])
    
    
    return results

    

def get_checkouts_for(remaining):
    double_finishes = __get_double_finishes()
    
    checkouts = get_checkouts_for_with_darts(remaining, 3)
    
    seen = set()
    filtered = []
    for checkout in checkouts:
        #print(checkout, end= " ")
        if len(checkout) == 3:
            checkout_id1 = f"{checkout[1][0]}-{checkout[2][0]}"
            checkout_id2 = f"{checkout[2][0]}-{checkout[1][0]}"
            if checkout_id1 not in seen:
                seen.add(checkout_id1)
                seen.add(checkout_id2)
                filtered.append(checkout)
                #print(f"Adding → {checkout}")
            #else:
                #print(f"Filtering out → {checkout}")
            
            
        else:
            filtered.append(checkout)
    
    #print(f"{len(checkouts)} → filtered: {len(filtered)}")  
        
    for checkout in filtered:
        print(f"\t{' '.join(list(map(lambda x: x[0], reversed(checkout))))}")




def get_all_checkouts():
    double_finishes = __get_double_finishes()
    #print(double_finishes)
    

    
    
    
    
    
#get_all_checkouts()
#get_checkouts_for(6)


for x in range(1, 170+1):
    #print(f"Checkouts for {x} → ", end="")
    print(f"Checkouts for {x}")
    get_checkouts_for(x)