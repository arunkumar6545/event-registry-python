from .Base import QueryParamsBase, QueryItems
import six


class _QueryCore(object):
    def __init__(self):
        self._queryObj = {}


    def getQuery(self):
        return self._queryObj


    def setQueryParam(self, paramName, val):
        self._queryObj[paramName] = val


    def _setValIfNotDefault(self, propName, value, defVal):
        if value != defVal:
            self._queryObj[propName] = value



class BaseQuery(_QueryCore):
    def __init__(self,
                 keyword = None,
                 conceptUri = None,
                 categoryUri = None,
                 sourceUri = None,
                 locationUri = None,
                 lang = None,
                 dateStart = None,
                 dateEnd = None,
                 dateMention = None,
                 sourceLocationUri = None,
                 sourceGroupUri=None,
                 authorUri = None,
                 keywordLoc = "body",
                 minMaxArticlesInEvent = None,
                 exclude = None):
        """
        @param keyword: keyword(s) to query. Either None, string or QueryItems instance
        @param conceptUri: concept(s) to query. Either None, string or QueryItems instance
        @param sourceUri: source(s) to query. Either None, string or QueryItems instance
        @param locationUri: location(s) to query. Either None, string or QueryItems instance
        @param categoryUri: categories to query. Either None, string or QueryItems instance
        @param lang: language(s) to query. Either None, string or QueryItems instance
        @param dateStart: starting date. Either None, string or date or datetime
        @param dateEnd: ending date. Either None, string or date or datetime
        @param dateMention: search by mentioned dates - Either None, string or date or datetime or a list of these types
        @param sourceLocationUri: find content generated by news sources at the specified geographic location - can be a city URI or a country URI. Multiple items can be provided using a list
        @param sourceGroupUri: a single or multiple source group URIs. A source group is a group of news sources, commonly defined based on common topic or importance
        @param authorUri: author(s) to query. Either None, string or QueryItems instance
        @param keywordLoc: where should we look when searching using the keywords provided by "keyword" parameter. "body" (default), "title", or "body,title"
        @param minMaxArticlesInEvent: a tuple containing the minimum and maximum number of articles that should be in the resulting events. Parameter relevant only if querying events
        @param exclude: a instance of BaseQuery, CombinedQuery or None. Used to filter out results matching the other criteria specified in this query
        """
        super(BaseQuery, self).__init__()

        self._setQueryArrVal("keyword", keyword)
        self._setQueryArrVal("conceptUri", conceptUri)
        self._setQueryArrVal("categoryUri", categoryUri)
        self._setQueryArrVal("sourceUri", sourceUri)
        self._setQueryArrVal("locationUri", locationUri)
        self._setQueryArrVal("lang", lang)

        # starting date of the published articles (e.g. 2014-05-02)
        if dateStart != None:
            self._queryObj["dateStart"] = QueryParamsBase.encodeDate(dateStart)
        # ending date of the published articles (e.g. 2014-05-02)
        if dateEnd != None:
            self._queryObj["dateEnd"] = QueryParamsBase.encodeDate(dateEnd)

        # mentioned date detected in articles (e.g. 2014-05-02)
        if dateMention != None:
            if isinstance(dateMention, list):
                self._queryObj["dateMention"] = [QueryParamsBase.encodeDate(d) for d in dateMention]
            else:
                self._queryObj["dateMention"] = QueryParamsBase.encodeDate(dateMention)

        self._setQueryArrVal("sourceLocationUri", sourceLocationUri)
        self._setQueryArrVal("sourceGroupUri", sourceGroupUri)
        self._setQueryArrVal("authorUri", authorUri)

        if keywordLoc != "body":
            self._queryObj["keywordLoc"] = keywordLoc

        if minMaxArticlesInEvent != None:
            assert isinstance(minMaxArticlesInEvent, tuple), "minMaxArticlesInEvent parameter should either be None or a tuple with two integer values"
            self._queryObj["minArticlesInEvent"] = minMaxArticlesInEvent[0]
            self._queryObj["maxArticlesInEvent"] = minMaxArticlesInEvent[1]

        if exclude != None:
            assert isinstance(exclude, (CombinedQuery, BaseQuery)), "exclude parameter was not a CombinedQuery or BaseQuery instance"
            self._queryObj["$not"] = exclude.getQuery()


    def _setQueryArrVal(self, propName, value):
        # by default we have None - so don't do anything
        if value is None:
            return
        # if we have an instance of QueryItems then apply it
        if isinstance(value, QueryItems):
            self._queryObj[propName] = { value.getOper(): value.getItems() }

        # if we have a string value, just use it
        elif isinstance(value, six.string_types):
            self._queryObj[propName] = value
        # there should be no other valid types
        else:
            assert False, "Parameter '%s' was of unsupported type. It should either be None, a string or an instance of QueryItems" % (propName)



class CombinedQuery(_QueryCore):
    def __init__(self):
        super(CombinedQuery, self).__init__()


    @staticmethod
    def AND(queryArr,
            exclude = None):
        """
        create a combined query with multiple items on which to perform an AND operation
        @param queryArr: a list of items on which to perform an AND operation. Items can be either a CombinedQuery or BaseQuery instances.
        @param exclude: a instance of BaseQuery, CombinedQuery or None. Used to filter out results matching the other criteria specified in this query
        """
        assert isinstance(queryArr, list), "provided argument as not a list"
        assert len(queryArr) > 0, "queryArr had an empty list"
        q = CombinedQuery()
        q.setQueryParam("$and", [])
        for item in queryArr:
            assert isinstance(item, (CombinedQuery, BaseQuery)), "item in the list was not a CombinedQuery or BaseQuery instance"
            q.getQuery()["$and"].append(item.getQuery())
        if exclude != None:
            assert isinstance(exclude, (CombinedQuery, BaseQuery)), "exclude parameter was not a CombinedQuery or BaseQuery instance"
            q.setQueryParam("$not", exclude.getQuery())
        return q


    @staticmethod
    def OR(queryArr,
           exclude = None):
        """
        create a combined query with multiple items on which to perform an OR operation
        @param queryArr: a list of items on which to perform an OR operation. Items can be either a CombinedQuery or BaseQuery instances.
        @param exclude: a instance of BaseQuery, CombinedQuery or None. Used to filter out results matching the other criteria specified in this query
        """
        assert isinstance(queryArr, list), "provided argument as not a list"
        assert len(queryArr) > 0, "queryArr had an empty list"
        q = CombinedQuery()
        q.setQueryParam("$or", [])
        for item in queryArr:
            assert isinstance(item, (CombinedQuery, BaseQuery)), "item in the list was not a CombinedQuery or BaseQuery instance"
            q.getQuery()["$or"].append(item.getQuery())
        if exclude != None:
            assert isinstance(exclude, (CombinedQuery, BaseQuery)), "exclude parameter was not a CombinedQuery or BaseQuery instance"
            q.setQueryParam("$not", exclude.getQuery())
        return q



class ComplexArticleQuery(_QueryCore):
    def __init__(self,
                 query,
                 dataType="news",
                 minSentiment=None,
                 maxSentiment=None,
                 minSocialScore=0,
                 minFacebookShares=0,
                 startSourceRankPercentile=0,
                 endSourceRankPercentile = 100,
                 isDuplicateFilter = "keepAll",
                 hasDuplicateFilter = "keepAll",
                 eventFilter = "keepAll"):
        """
        create an article query using a complex query
        @param query: an instance of CombinedQuery or BaseQuery to use to find articles that match the conditions
        @param dataType: data type to search for. Possible values are "news" (news content), "pr" (PR content) or "blogs".
                If you want to use multiple data types, put them in an array (e.g. ["news", "pr"])
        @param minSentiment: what should be the minimum sentiment on the articles in order to return them (None means that we don't filter by sentiment)
        @param maxSentiment: what should be the maximum sentiment on the articles in order to return them (None means that we don't filter by sentiment)
        @param minSocialScore: at least how many times should the articles be shared on social media in order to return them
        @param minFacebookShares: at least how many times should the articles be shared on Facebook in order to return them
        @param startSourceRankPercentile: starting percentile of the sources to consider in the results (default: 0). Value should be in range 0-90 and divisible by 10.
        @param endSourceRankPercentile: ending percentile of the sources to consider in the results (default: 100). Value should be in range 10-100 and divisible by 10.
        @param isDuplicateFilter: some articles can be duplicates of other articles. What should be done with them. Possible values are:
                "skipDuplicates" (skip the resulting articles that are duplicates of other articles)
                "keepOnlyDuplicates" (return only the duplicate articles)
                "keepAll" (no filtering, default)
        @param hasDuplicateFilter: some articles are later copied by others. What should be done with such articles. Possible values are:
                "skipHasDuplicates" (skip the resulting articles that have been later copied by others)
                "keepOnlyHasDuplicates" (return only the articles that have been later copied by others)
                "keepAll" (no filtering, default)
        @param eventFilter: some articles describe a known event and some don't. This filter allows you to filter the resulting articles based on this criteria.
                Possible values are:
                "skipArticlesWithoutEvent" (skip articles that are not describing any known event in ER)
                "keepOnlyArticlesWithoutEvent" (return only the articles that are not describing any known event in ER)
                "keepAll" (no filtering, default)
        """
        super(ComplexArticleQuery, self).__init__()

        assert isinstance(query, (CombinedQuery, BaseQuery)), "query parameter was not a CombinedQuery or BaseQuery instance"
        self._queryObj["$query"] = query.getQuery()
        filter = {}
        if dataType != "news":
            filter["dataType"] = dataType

        if minSentiment != None:
            filter["minSentiment"] = minSentiment
        if maxSentiment != None:
            filter["maxSentiment"] = maxSentiment

        if minSocialScore > 0:
            filter["minSocialScore"] = minSocialScore
        if minFacebookShares > 0:
            filter["minFacebookShares"] = minFacebookShares
        if startSourceRankPercentile != 0:
            filter["startSourceRankPercentile"] = startSourceRankPercentile
        if endSourceRankPercentile != 100:
            filter["endSourceRankPercentile"] = endSourceRankPercentile

        if isDuplicateFilter != "keepAll":
            filter["isDuplicate"] = isDuplicateFilter
        if hasDuplicateFilter != "keepAll":
            filter["hasDuplicate"] = hasDuplicateFilter
        if eventFilter != "keepAll":
            filter["hasEvent"] = eventFilter

        if len(filter) > 0:
            self._queryObj["$filter"] = filter



class ComplexEventQuery(_QueryCore):
    def __init__(self,
                query,
                minSentiment=None,
                maxSentiment=None):
        """
        create an event query using a complex query
        @param query: an instance of CombinedQuery or BaseQuery to use to find events that match the conditions
        """
        super(ComplexEventQuery, self).__init__()

        assert isinstance(query, (CombinedQuery, BaseQuery)), "query parameter was not a CombinedQuery or BaseQuery instance"
        filter = {}
        if minSentiment != None:
            filter["minSentiment"] = minSentiment
        if maxSentiment != None:
            filter["maxSentiment"] = maxSentiment

        if len(filter) > 0:
            self._queryObj["$filter"] = filter
        self._queryObj["$query"] = query.getQuery()
