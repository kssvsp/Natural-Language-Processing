import re


from sklearn import tree
from sklearn import preprocessing

from sklearn.metrics import accuracy_score

def split_text(path):
    ts=open(path)
    d = ts.readlines()
    ts.close()
    ts_write=open(path,"w")
    try:
        for i in d:
            if(i[-4:].strip().__eq__("TOK")):
                j = re.split("\s", i)
                j1 = str(j[1])
                p = re.findall("[^\w\s]", j1)
                if(len(p) < 1):
                    ts_write.write(i)
            else:
                ts_write.write(i)
    except:
        print("except")

    ts_write.close()


    ts=open(path)
    l1 = []
    try:
        for i in ts:
            if(i[-4:].strip().__eq__("EOS")):
                d=next(ts)
                l1.append(i)
                l1.append(d)
    except:
        print("exception")


    line_count = 0
    final_lst = []
    try:
        for i in l1:
            if(i[-4:].strip().__eq__('EOS')):
                j = re.split("\s", i)
                x = str(j[1])
                s = re.sub(r'[^\w\s]', '', x)
                x = j[0]+" "+s+". "+j[2]
                j1 = re.split("\s", l1[line_count+1])
                r = s+"."+j1[1]
                dot_st = r+" "+j[2]
                final_lst.append(dot_st)
            line_count = line_count + 1
    except:
        print("exception")

#print(final_lst)

    final_ts = []
    class_values = []
    for i in final_lst:
        target_values = []
        split_space = re.split("\s", i)
        if(split_space[1].strip().__eq__("EOS")):
            class_values.append(1)
        else:
            class_values.append(0)
        final_split = split_space[0].split(".")
        left_wrd = str(final_split[0])
        right_wrd = str(final_split[1])
        target_values.append(left_wrd)
        target_values.append(right_wrd)
        if(len(final_split[0])<3):
            target_values.append(1)
        else:
            target_values.append(0)
        left_cap = re.findall("[A-Z]",left_wrd)
        if(len(left_cap)>0):
            target_values.append(1)
        else:
            target_values.append(0)
        right_cap = re.findall("[A-Z]",right_wrd)
        if(len(right_cap)>0):
            target_values.append(1)
        else:
            target_values.append(0)
        if re.match("^[The]*[A]*[An]$", right_wrd):
            target_values.append(1)
        else:
            target_values.append(0)
        if re.match("[0-9]", right_wrd):
            target_values.append(1)
        else:
            target_values.append(0)
        if re.match("[0-9]", left_wrd):
            target_values.append(1)
        else:
            target_values.append(0)
        final_ts.append(target_values)
    print(final_ts)
    return final_ts, class_values

def encode(encode_set, class_values):
    num_elements = len(class_values)
    print(encode_set)
    for i in range(0, num_elements):
        encode_set[i].append(class_values[i])
    data = []
    for value in encode_set:
        encoder = preprocessing.LabelEncoder()
        value = encoder.fit_transform(value)
        data.append(value)

    x_value = [[x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]] for x in data]
    y_value = [x[8] for x in data]
    print(len(x_value))
    print(len(y_value))
    return x_value, y_value

def train_classifier(x_train, y_train):
    clf = tree.DecisionTreeClassifier(criterion="entropy", random_state=100)
    clf.fit(x_train, y_train)
    dot_data = tree.export_graphviz(clf, out_file='tree.dot')
    print(clf)
    return clf



def prediction(x_test, clf_object):
    y_pred = clf_object.predict(x_test)
    print("Predicted values:")
    return y_pred


def main():
    file_name = "C:/Users/priya/Downloads/SBDtrain.txt"
    x, y = split_text(file_name)
    a, b = encode(x, y)
    classy = train_classifier(a, b)
    test_file = "C:/Users/priya/Downloads/SBDtest.txt"
    x_1, y_1 = split_text(test_file)
    a_1, b_1 = encode(x_1, y_1)
    y_pred = prediction(a_1, classy)
    test_acc = accuracy_score(b_1, y_pred)*100
    print("Accuracy : ", test_acc)

if __name__ == "__main__":
    main()