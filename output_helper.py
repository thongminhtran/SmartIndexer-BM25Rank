def DisplayingPairsWithDocsID(docStream):
    doc = next(docStream, None)
    docs_count = 0
    while doc is not None:
        docsID, token_list = doc
        for token in token_list:
            if token != '':
                yield docsID, token
        docs_count += 1
        doc = next(docStream, None)
    print(str(docs_count) + ' documents that have been processed')

