import sys

def get_postings(inverted_index, term, output_file):
  tmp = inverted_index[term]
  with open(output_file, 'a') as f:
    print('GetPostings', file=f)
    print(term, file=f)
    print('Postings list: ', end='', file=f)
    print(*tmp, end = '', file=f)
    print(file=f)

def daatAnd(inverted_index, queries, output_file):
  lists = []
  for query in queries:
    lists.append(inverted_index[query])
  
  if (len(lists) > 0):
    lists = sorted(lists, key=len)
    indexes = []
    for i in range(len(queries)):
      indexes.append(0)
  
    results_list = []
    is_present = False
    comparisons = 0
    num_present = 1

    for doc in lists[0]:
      for i, temp in enumerate(lists[1:]):
        if indexes[i+1] >= len(temp):
            continue
        diff = doc - temp[indexes[i+1]]
        comparisons += 1
        if (diff < 0):
          break
        elif (diff == 0):
           num_present += 1
           indexes[i+1] += 1
           continue
        else:
          while ((indexes[i+1] < len(temp)) and (diff >0)):
            indexes[i+1] += 1
            if (indexes[i+1] < len(temp)):
              diff = doc - temp[indexes[i+1]]
              comparisons += 1
          if (diff < 0):
            break
          elif (diff == 0):
            num_present+= 1
            indexes[i+1] += 1
          else:
            break           
      if num_present == len(lists):
        is_present =True
      if is_present:
        results_list.append(doc)
        is_present = False
      num_present = 1

  with open(output_file, 'a') as f:
    print('DaatAnd',file=f)
    print(*queries, end='', file=f)
    print(file=f)
    print('Results: ', end = '', file=f)
    if len(results_list) == 0:
      print('empty', end='', file=f)
    else:
      print(*results_list, end = '', file=f)
    print(file=f)
    print('Number of documents in results:', len(results_list), file = f)
    print('Number of comparisons:', comparisons, file=f)

    return results_list

def daatOr(inverted_index, queries, output_file):
  lists = []
  for query in queries:
    lists.append(inverted_index[query])
 
  indexes = []
  for i in range(len(queries)):
    indexes.append(0)
  
  comparisons = 0
  min_value_indexes = []
  results_list = []
  min_value = None
  
  while(True):
    for i, postin_list in enumerate(lists):
      if indexes[i] >= len(postin_list):
        continue
      else:
        if min_value == None:
          min_value = postin_list[indexes[i]]
          min_value_indexes.append(i)
        else:
          tmp = min_value - postin_list[indexes[i]]
          comparisons += 1
          if (tmp == 0):
            min_value_indexes.append(i)
          elif (tmp > 0): # CURRNET MIN > ELEMENT WE'RE COMPARING
            min_value = postin_list[indexes[i]]
            min_value_indexes = []
            min_value_indexes.append(i)
    if min_value != None:
      results_list.append(min_value)
      min_value = None
      for index in min_value_indexes:
        indexes[index] += 1
      min_value_indexes = []
    else:
      break
  with open(output_file, 'a') as f:
    print('DaatOr',file=f)
    print(*queries, end='', file=f)
    print(file=f)
    print('Results: ', end = '', file=f)
    if len(results_list) == 0:
      print('empty', end = '', file=f)
    else:
       print(*results_list, end = '', file=f)
    print(file=f)
    print('Number of documents in results:', len(results_list), file = f)
    print('Number of comparisons:', comparisons, file=f)

    return results_list

def tf_idf(inverted_index, position_index, results, queries, N):
  tf_idfs = []
  tf, idf, tf_idf  = 0, 0, 0
  for result in results:
    for query in queries:
      if result in position_index[query]:
        tfs = position_index[query][result][0]
        total_words = position_index[query][result][1]
        tf = (tfs / total_words)
        idf = (N / len(inverted_index[query]))
      else:
        tf = 0
        idf = (N / len(inverted_index[query]))
      tf_idf += tf * idf        
    tf_idfs.append(tf_idf)
    tf_idf = 0
  
  tmp = {}
  for res, tf_idf1 in zip(results, tf_idfs):
    tmp[res] = tf_idf1
  tmp = sorted(tmp.items(), key=lambda x:x[1], reverse=True)
  #print(tmp)
  with open(output_file, 'a') as f:
    print('TF-IDF',file=f)
    print('Results: ', end = '', file=f)
    if len(tmp) == 0:
      print('empty', end = '', file=f)
    else:
      docs = []
      for i in tmp:
        docs.append(i[0])
      print(*docs, end='', file=f)
    print(file=f)
    
def create_position_index(filename):
  position_index = {}
  with open(filename, 'r') as f:
    buffer = f.readline()
    while buffer:
      terms  = buffer.split()
      doc_ID = int(terms[0])
      #print(doc_ID)
      terms_set = set(terms[1:]) 
      for term in terms_set:
        count = 0
        if term not in position_index:
          position_index[term] = {}
        
        tmp = []
        for term1 in terms:
          if term == term1:
            count += 1
        tmp.append(count)
        tmp.append(len(terms[1:]))
        position_index[term][doc_ID] = tmp
             
      buffer = f.readline()
  return position_index

def create_inverted_index(filename):
  N = 0
  inverted_index = {}
  with open(filename, 'r') as f:
    buffer = f.readline()
    while buffer:
      N += 1
      terms  = buffer.split()
      doc_ID = int(terms[0])
      #print(doc_ID)
      for term in terms[1:]:
        if term in inverted_index:
          if doc_ID not in inverted_index[term]:
             inverted_index[term].append(doc_ID)
        else:
          inverted_index[term] = []
          inverted_index[term].append(doc_ID)
      buffer = f.readline()
  return inverted_index, N

if __name__ == '__main__':
  filename = sys.argv[1]
  inverted_index, N = create_inverted_index(filename)
  # print(N)
  # print(len(inverted_index))
  #print(inverted_index)

  input_file = sys.argv[3]
  output_file = sys.argv[2]

  position_index = create_position_index(filename)
  #print(position_index, '\n\n')

  with open(input_file, 'r') as f:
    buffer = f.readline()
    count = 0
    while buffer:
      if (count > 0):
        with open(output_file, 'a') as g:
          print(file=g)
      for term in buffer.split():
        get_postings(inverted_index, term, output_file)
      results = daatAnd(inverted_index, buffer.split(), output_file)
      tf_idf(inverted_index, position_index, results, buffer.split(), N)
      results1 = daatOr(inverted_index, buffer.split(), output_file)
      tf_idf(inverted_index, position_index, results1, buffer.split(), N)
      count+=1
      buffer = f.readline()