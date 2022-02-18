import time
import concurrent.futures


def spitter(inputs):
    return(inputs.strip() +' :Processed')

def fileOpener(fileName):
    file = open(fileName, 'r', encoding='UTF-8')
    fileItems = file.readlines()
    return fileItems

def main(items, workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for item in items:
            futures.append(executor.submit(spitter, inputs=item))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


itemList = fileOpener('fileName.txt')
totalItems = len(itemList)
countTotal = 0
countBatch = 0
batch = 23      #Set the batch size per cycle

while True:
    if countBatch < batch:
        batchList = itemList[countTotal:countTotal+batch]
        main(batchList)
        countBatch += batch
        countTotal += batch

    if countBatch == batch:
        print('One Batch Completed')
        countBatch = 0
        if countTotal >= totalItems:
            break

