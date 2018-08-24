﻿import six, json
from eventregistry.Base import *
from eventregistry.ReturnInfo import *
from eventregistry.Query import *


class QueryEvents(Query):
    def __init__(self,
                 keywords = None,
                 conceptUri = None,
                 categoryUri = None,
                 sourceUri = None,
                 sourceLocationUri = None,
                 sourceGroupUri = None,
                 authorUri = None,
                 locationUri = None,
                 lang = None,
                 dateStart = None,
                 dateEnd = None,
                 minArticlesInEvent = 0,
                 maxArticlesInEvent = sys.maxsize,
                 dateMentionStart = None,
                 dateMentionEnd = None,
                 ignoreKeywords = None,
                 ignoreConceptUri = None,
                 ignoreCategoryUri = None,
                 ignoreSourceUri = None,
                 ignoreSourceLocationUri = None,
                 ignoreSourceGroupUri = None,
                 ignoreAuthorUri = None,
                 ignoreLocationUri = None,
                 ignoreLang = None,
                 keywordsLoc = "body",
                 ignoreKeywordsLoc = "body",
                 requestedResult = None):
        """
        Query class for searching for events in the Event Registry.
        The resulting events have to match all specified conditions. If a parameter value equals "" or [], then it is ignored.
        In order for query to be valid, it has to have at least one positive condition (condition that does not start with ignore*).

        @param keywords: find events where articles mention all the specified keywords.
            A single keyword/phrase can be provided as a string, multiple keywords/phrases can be provided as a list of strings.
            Use QueryItems.AND() if *all* provided keywords/phrases should be mentioned, or QueryItems.OR() if *any* of the keywords/phrases should be mentioned.
        @param conceptUri: find events where the concept with concept uri is important.
            A single concept uri can be provided as a string, multiple concept uris can be provided as a list of strings.
            Use QueryItems.AND() if *all* provided concepts should be mentioned, or QueryItems.OR() if *any* of the concepts should be mentioned.
            To obtain a concept uri using a concept label use EventRegistry.getConceptUri().
        @param categoryUri: find events that are assigned into a particular category.
            A single category uri can be provided as a string, multiple category uris can be provided as a list of strings.
            Use QueryItems.AND() if *all* provided categories should be mentioned, or QueryItems.OR() if *any* of the categories should be mentioned.
            A category uri can be obtained from a category name using EventRegistry.getCategoryUri().
        @param sourceUri: find events that contain one or more articles that have been written by a news source sourceUri.
            If multiple sources should be considered use QueryItems.OR() to provide the list of sources.
            Source uri for a given news source name can be obtained using EventRegistry.getNewsSourceUri().
        @param sourceLocationUri: find events that contain one or more articles that were written by news sources located in the given geographic location.
            If multiple source locations are provided, then put them into a list inside QueryItems.OR()
            Location uri can either be a city or a country. Location uri for a given name can be obtained using EventRegistry.getLocationUri().
        @param sourceGroupUri: find events that contain one or more articles that were written by news sources that are assigned to the specified source group.
            If multiple source groups are provided, then put them into a list inside QueryItems.OR()
            Source group uri for a given name can be obtained using EventRegistry.getSourceGroupUri().
        @param authorUri: find events that contain one or more articles that have been written by a specific author.
            If multiple authors should be considered use QueryItems.OR() or QueryItems.AND() to provide the list of authors.
            Author uri for a given author name can be obtained using EventRegistry.getAuthorUri().
        @param locationUri: find events that occured at a particular location.
            If value can be a string or a list of strings provided in QueryItems.OR().
            Location uri can either be a city or a country. Location uri for a given name can be obtained using EventRegistry.getLocationUri().
        @param lang: find events for which we found articles in the specified language.
            If more than one language is specified, resulting events has to be reported in *any* of the languages.
        @param dateStart: find events that occured on or after dateStart. Date should be provided in YYYY-MM-DD format, datetime.time or datetime.datetime.
        @param dateEnd: find events that occured before or on dateEnd. Date should be provided in YYYY-MM-DD format, datetime.time or datetime.datetime.
        @param minArticlesInEvent: find events that have been reported in at least minArticlesInEvent articles (regardless of language)
        @param maxArticlesInEvent: find events that have not been reported in more than maxArticlesInEvent articles (regardless of language)
        @param dateMentionStart: find events where articles explicitly mention a date that is equal or greater than dateMentionStart.
        @param dateMentionEnd: find events where articles explicitly mention a date that is lower or equal to dateMentionEnd.
        @param ignoreKeywords: ignore events where articles about the event mention any of the provided keywords
        @param ignoreConceptUri: ignore events that are about any of the provided concepts
        @param ignoreCategoryUri: ignore events that are about any of the provided categories
        @param ignoreSourceUri: ignore events that have have articles which have been written by any of the specified news sources
        @param ignoreSourceLocationUri: ignore events that have articles which been written by sources located at *any* of the specified locations
        @param ignoreSourceGroupUri: ignore events that have articles which have been written by sources in *any* of the specified source groups
        @param ignoreAuthorUri: ignore articles that were written by *any* of the specified authors
        @param ignoreLocationUri: ignore events that occured in any of the provided locations. A location can be a city or a place
        @param ignoreLang: ignore events that are reported in any of the provided languages
        @param keywordsLoc: what data should be used when searching using the keywords provided by "keywords" parameter. "body" (default), "title", or "body,title"
        @param ignoreKeywordsLoc: what data should be used when searching using the keywords provided by "ignoreKeywords" parameter. "body" (default), "title", or "body,title"
        @param requestedResult: the information to return as the result of the query. By default return the list of matching events
        """
        super(QueryEvents, self).__init__()

        self._setVal("action", "getEvents")

        self._setQueryArrVal(keywords, "keyword", "keywordOper", "and")
        self._setQueryArrVal(conceptUri, "conceptUri", "conceptOper", "and")
        self._setQueryArrVal(categoryUri, "categoryUri", "categoryOper", "or")
        self._setQueryArrVal(sourceUri, "sourceUri", "sourceOper", "or")
        self._setQueryArrVal(sourceLocationUri, "sourceLocationUri", None, "or")
        self._setQueryArrVal(sourceGroupUri, "sourceGroupUri", "sourceGroupOper", "or")
        self._setQueryArrVal(authorUri, "authorUri", "authorOper", "or")
        self._setQueryArrVal(locationUri, "locationUri", None, "or")        # location such as "http://en.wikipedia.org/wiki/Ljubljana"

        self._setQueryArrVal(lang, "lang", None, "or")                      # a single lang or list (possible: eng, deu, spa, zho, slv)

        if (dateStart != None):
            self._setDateVal("dateStart", dateStart)   # 2014-05-02
        if (dateEnd != None):
            self._setDateVal("dateEnd", dateEnd)       # 2014-05-02

        self._setValIfNotDefault("minArticlesInEvent", minArticlesInEvent, 0)
        self._setValIfNotDefault("maxArticlesInEvent", maxArticlesInEvent, sys.maxsize)

        if (dateMentionStart != None):
            self._setDateVal("dateMentionStart", dateMentionStart)    # e.g. 2014-05-02
        if (dateMentionEnd != None):
            self._setDateVal("dateMentionEnd", dateMentionEnd)        # e.g. 2014-05-02

        # for the negative conditions, only the OR is a valid operator type
        self._setQueryArrVal(ignoreKeywords, "ignoreKeywords", None, "or")
        self._setQueryArrVal(ignoreConceptUri, "ignoreConceptUri", None, "or")
        self._setQueryArrVal(ignoreCategoryUri, "ignoreCategoryUri", None, "or")
        self._setQueryArrVal(ignoreSourceUri, "ignoreSourceUri", None, "or")
        self._setQueryArrVal(ignoreSourceLocationUri, "ignoreSourceLocationUri", None, "or")
        self._setQueryArrVal(ignoreSourceGroupUri, "ignoreSourceGroupUri", None, "or")
        self._setQueryArrVal(ignoreAuthorUri, "ignoreAuthorUri", None, "or")
        self._setQueryArrVal(ignoreLocationUri, "ignoreLocationUri", None, "or")

        self._setQueryArrVal(ignoreLang, "ignoreLang", None, "or")

        self._setValIfNotDefault("keywordLoc", keywordsLoc, "body")
        self._setValIfNotDefault("ignoreKeywordLoc", ignoreKeywordsLoc, "body")

        self.setRequestedResult(requestedResult or RequestEventsInfo())


    def _getPath(self):
        return "/json/event"


    def setRequestedResult(self, requestEvents):
        """
        Set the single result type that you would like to be returned. Any previously set result types will be overwritten.
        Result types can be the classes that extend RequestEvents base class (see classes below).
        """
        assert isinstance(requestEvents, RequestEvents), "QueryEvents class can only accept result requests that are of type RequestEvents"
        self.resultTypeList = [requestEvents]


    @staticmethod
    def initWithEventUriList(uriList):
        """
        Set a custom list of event uris. The results will be then computed on this list - no query will be done (all conditions will be ignored).
        """
        q = QueryEvents()
        assert isinstance(uriList, list), "uriList has to be a list of strings that represent event uris"
        q.queryParams = { "action": "getEvents", "eventUriList": ",".join(uriList) }
        return q


    @staticmethod
    def initWithEventUriWgtList(uriWgtList):
        """
        Set a custom list of event uris. The results will be then computed on this list - no query will be done (all conditions will be ignored).
        """
        q = QueryEvents()
        assert isinstance(uriWgtList, list), "uriWgtList has to be a list of strings that represent event uris with their weights"
        q.queryParams = { "action": "getEvents", "eventUriWgtList": ",".join(uriWgtList) }
        return q


    @staticmethod
    def initWithComplexQuery(query):
        """
        create a query using a complex event query
        """
        q = QueryEvents()
        # provided an instance of ComplexEventQuery
        if isinstance(query, ComplexEventQuery):
            q._setVal("query", json.dumps(query.getQuery()))
        # provided query as a string containing the json object
        elif isinstance(query, six.string_types):
            foo = json.loads(query)
            q._setVal("query", query)
        # provided query as a python dict
        elif isinstance(query, dict):
            q._setVal("query", json.dumps(query))
        # unrecognized value provided
        else:
            assert False, "The instance of query parameter was not a ComplexEventQuery, a string or a python dict"
        return q



class QueryEventsIter(QueryEvents, six.Iterator):
    """
    class that simplifies and combines functionality from QueryEvents and RequestEventsInfo. It provides an iterator
    over the list of events that match the specified conditions
    """

    def count(self, eventRegistry):
        """
        return the number of events that match the criteria
        """
        self.setRequestedResult(RequestEventsInfo())
        res = eventRegistry.execQuery(self)
        if "error" in res:
            print(res["error"])
        count = res.get("events", {}).get("totalResults", 0)
        return count


    def execQuery(self, eventRegistry,
                  sortBy = "rel",
                  sortByAsc = False,
                  returnInfo = ReturnInfo(),
                  maxItems = -1,
                  **kwargs):
        """
        @param eventRegistry: instance of EventRegistry class. used to query new event list and uris
        @param sortBy: how should the resulting events be sorted. Options: date (by event date), rel (relevance to the query), size (number of articles),
            socialScore (amount of shares in social media), none (no specific sorting)
        @param sortByAsc: should the results be sorted in ascending order (True) or descending (False)
        @param returnInfo: what details should be included in the returned information
        @param maxItems: maximum number of items to be returned. Used to stop iteration sooner than results run out
        """
        self._er = eventRegistry
        self._sortBy = sortBy
        self._sortByAsc = sortByAsc
        self._returnInfo = returnInfo
        self._eventBatchSize = 50      # always download max - best for the user since it uses his token and we want to download as much as possible in a single search
        self._eventPage = 0
        self._totalPages = None
        # if we want to return only a subset of items:
        self._maxItems = maxItems
        self._currItem = 0
        # list of cached events that are yet to be returned by the iterator
        self._eventList = []
        return self


    @staticmethod
    def initWithComplexQuery(query):
        q = QueryEventsIter()
        # provided an instance of ComplexEventQuery
        if isinstance(query, ComplexEventQuery):
            q._setVal("query", json.dumps(query.getQuery()))
        # provided query as a string containing the json object
        elif isinstance(query, six.string_types):
            foo = json.loads(query)
            q._setVal("query", query)
        # provided query as a python dict
        elif isinstance(query, dict):
            q._setVal("query", json.dumps(query))
        else:
            assert False, "The instance of query parameter was not a ComplexEventQuery, a string or a python dict"
        return q


    def _getNextEventBatch(self):
        """download next batch of events based on the event uris in the uri list"""
        self._eventPage += 1
        # if we have already obtained all pages, then exit
        if self._totalPages != None and self._eventPage > self._totalPages:
            return
        self.setRequestedResult(RequestEventsInfo(page=self._eventPage, count=self._eventBatchSize,
            sortBy= self._sortBy, sortByAsc=self._sortByAsc,
            returnInfo = self._returnInfo))
        # download articles and make sure that we set the same archive flag as it was returned when we were processing the uriList request
        if self._er._verboseOutput:
            print("Downloading event page %d..." % (self._eventPage))
        res = self._er.execQuery(self)
        if "error" in res:
            print("Error while obtaining a list of events: " + res["error"])
        else:
            self._totalPages = res.get("events", {}).get("pages", 0)
        results = res.get("events", {}).get("results", [])
        self._eventList.extend(results)


    def __iter__(self):
        return self


    def __next__(self):
        """iterate over the available events"""
        self._currItem += 1
        # if we want to return only the first X items, then finish once reached
        if self._maxItems >= 0 and self._currItem > self._maxItems:
            raise StopIteration
        if len(self._eventList) == 0:
            self._getNextEventBatch()
        if len(self._eventList) > 0:
            return self._eventList.pop(0)
        raise StopIteration



class RequestEvents:
    def __init__(self):
        self.resultType = None


    def getResultType(self):
        return self.resultType



class RequestEventsInfo(RequestEvents):
    def __init__(self, page = 1,
                 count = 50,
                 sortBy = "rel", sortByAsc = False,
                 returnInfo = ReturnInfo()):
        """
        return event details for resulting events
        @param page: page of the results to return (1, 2, ...)
        @param count: number of events to return per page (at most 50)
        @param sortBy: how should the resulting events be sorted. Options: date (by event date), rel (relevance to the query), size (number of articles),
            socialScore (amount of shares in social media), none (no specific sorting)
        @param sortByAsc: should the results be sorted in ascending order (True) or descending (False)
        @param returnInfo: what details should be included in the returned information
        """
        assert page >= 1, "page has to be >= 1"
        assert count <= 50, "at most 50 events can be returned per call"
        self.resultType = "events"
        self.eventsPage = page
        self.eventsCount = count
        self.eventsSortBy = sortBy
        self.eventsSortByAsc = sortByAsc
        self.__dict__.update(returnInfo.getParams("events"))


    def setPage(self, page):
        assert page >= 1, "page has to be >= 1"
        self.eventsPage = page


    def setCount(self, count):
        self.eventsCount = count



class RequestEventsUriWgtList(RequestEvents):
    def __init__(self,
                 page = 1,
                 count = 50000,
                 sortBy = "rel", sortByAsc = False):
        """
        return a simple list of event uris together with the scores for resulting events
        @param page: page of the results (1, 2, ...)
        @param count: number of results to include per page (at most 100000)
        @param sortBy: how should the resulting events be sorted. Options: date (by event date), rel (relevance to the query), size (number of articles),
            socialScore (amount of shares in social media), none (no specific sorting)
        @param sortByAsc: should the events be sorted in ascending order (True) or descending (False)
        """
        assert page >= 1, "page has to be >= 1"
        assert count <= 100000
        self.resultType = "uriWgtList"
        self.uriWgtListPage = page
        self.uriWgtListCount = count
        self.uriWgtListSortBy = sortBy
        self.uriWgtListSortByAsc = sortByAsc

    def setPage(self, page):
        assert page >= 1, "page has to be >= 1"
        self.uriWgtListPage = page



class RequestEventsTimeAggr(RequestEvents):
    def __init__(self):
        """
        return time distribution of resulting events
        """
        self.resultType = "timeAggr"



class RequestEventsKeywordAggr(RequestEvents):
    def __init__(self, lang = None):
        """
        return keyword aggregate (tag cloud) on words in articles in resulting events
        @param lang: in which language to produce the list of top keywords. If None, then compute on all articles
        """
        self.resultType = "keywordAggr"
        if lang != None:
            self.keywordAggrLang = lang



class RequestEventsLocAggr(RequestEvents):
    def __init__(self,
                 eventsSampleSize = 100000,
                 returnInfo = ReturnInfo()):
        """
        return aggreate of locations of resulting events
        @param eventsSampleSize: sample of events to use to compute the location aggregate (at most 100000)
        @param returnInfo: what details (about locations) should be included in the returned information
        """
        assert eventsSampleSize <= 100000
        self.resultType = "locAggr"
        self.locAggrSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("locAggr"))



class RequestEventsLocTimeAggr(RequestEvents):

    def __init__(self,
                 eventsSampleSize = 100000,
                 returnInfo = ReturnInfo()):
        """
        return aggreate of locations and times of resulting events
        @param eventsSampleSize: sample of events to use to compute the location aggregate (at most 100000)
        @param returnInfo: what details (about locations) should be included in the returned information
        """
        assert eventsSampleSize <= 100000
        self.resultType = "locTimeAggr"
        self.locTimeAggrSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("locTimeAggr"))



class RequestEventsConceptAggr(RequestEvents):
    def __init__(self,
                 conceptCount = 20,
                 eventsSampleSize = 100000,
                 returnInfo = ReturnInfo()):
        """
        compute which concept are the most frequently occuring in the list of resulting events
        @param conceptCount: number of top concepts to return (at most 200)
        @param eventsSampleSize: on what sample of results should the aggregate be computed (at most 1000000)
        @param returnInfo: what details about the concepts should be included in the returned information
        """
        assert conceptCount <= 200
        assert eventsSampleSize <= 1000000
        self.resultType = "conceptAggr"
        self.conceptAggrConceptCount = conceptCount
        self.conceptAggrSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("conceptAggr"))



class RequestEventsConceptGraph(RequestEvents):
    def __init__(self,
                 conceptCount = 50,
                 linkCount = 150,
                 eventsSampleSize = 50000,
                 returnInfo = ReturnInfo()):
        """
        compute which concept pairs frequently co-occur together in the resulting events
        @param conceptCount: number of top concepts to return (at most 1,000)
        @param linkCount: number of links between the concepts to return (at most 2,000)
        @param eventsSampleSize: on what sample of results should the aggregate be computed (at most 100000)
        @param returnInfo: what details about the concepts should be included in the returned information
        """
        assert conceptCount <= 1000
        assert linkCount <= 2000
        assert eventsSampleSize <= 300000
        self.resultType = "conceptGraph"
        self.conceptGraphConceptCount = conceptCount
        self.conceptGraphLinkCount = linkCount
        self.conceptGraphSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("conceptGraph"))



class RequestEventsConceptMatrix(RequestEvents):
    def __init__(self,
                 conceptCount = 25,
                 measure = "pmi",
                 eventsSampleSize = 100000,
                 returnInfo = ReturnInfo()):
        """
        get a matrix of concepts and their dependencies. For individual concept pairs
        return how frequently they co-occur in the resulting events and
        how "surprising" this is, based on the frequency of individual concepts
        @param conceptCount: number of top concepts to return (at most 200)
        @param measure: how should the interestingness between the selected pairs of concepts be computed. Options: pmi (pointwise mutual information), pairTfIdf (pair frequence * IDF of individual concepts), chiSquare
        @param eventsSampleSize: on what sample of results should the aggregate be computed (at most 300000)
        @param returnInfo: what details about the concepts should be included in the returned information
        """
        assert conceptCount <= 200
        assert eventsSampleSize <= 300000
        self.resultType = "conceptMatrix"
        self.conceptMatrixConceptCount = conceptCount
        self.conceptMatrixMeasure = measure
        self.conceptMatrixSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("conceptMatrix"))



class RequestEventsConceptTrends(RequestEvents):
    def __init__(self,
                 conceptUris = None,
                 conceptCount = 10,
                 returnInfo = ReturnInfo()):
        """
        return a list of top trending concepts and their daily trending info over time
        @param conceptUris: list of concept URIs for which to return trending information. If None, then top concepts will be automatically computed
        @param count: if the concepts are not provided, what should be the number of automatically determined concepts to return (at most 50)
        @param returnInfo: what details about the concepts should be included in the returned information
        """
        assert conceptCount <= 50
        self.resultType = "conceptTrends"
        if conceptUris != None:
            self.conceptTrendsConceptUri = conceptUris
        self.conceptTrendsConceptCount = conceptCount
        self.__dict__.update(returnInfo.getParams("conceptTrends"))



class RequestEventsSourceAggr(RequestEvents):
    def __init__(self,
                 sourceCount = 30,
                 eventsSampleSize = 50000,
                 returnInfo = ReturnInfo()):
        """
        return top news sources that report about the events that match the search conditions
        @param sourceCount: number of top sources to return (at most 200)
        @param eventsSampleSize: on what sample of results should the aggregate be computed (at most 300000)
        @param returnInfo: what details about the sources should be included in the returned information
        """
        assert sourceCount <= 200
        assert eventsSampleSize <= 100000
        self.resultType = "sourceAggr"
        self.sourceAggrSourceCount = sourceCount
        self.sourceAggrSampleSize = eventsSampleSize
        self.__dict__.update(returnInfo.getParams("sourceAggr"))



class RequestEventsDateMentionAggr(RequestEvents):
    def __init__(self,
                 minDaysApart = 0,
                 minDateMentionCount = 5,
                 eventsSampleSize = 100000):
        """
        return events and the dates that are mentioned in articles about these events
        @param minDaysApart: ignore events that don't have a date that is more than this number of days apart from the tested event
        @param minDateMentionCount: report only dates that are mentioned at least this number of times
        @param eventsSampleSize: on what sample of results should the aggregate be computed (at most 300000)
        """
        assert eventsSampleSize <= 300000
        self.resultType = "dateMentionAggr"
        self.dateMentionAggrMinDaysApart = minDaysApart
        self.dateMentionAggrMinDateMentionCount = minDateMentionCount
        self.dateMentionAggrSampleSize = eventsSampleSize



class RequestEventsEventClusters(RequestEvents):
    def __init__(self,
                 keywordCount = 30,
                 maxEventsToCluster = 10000,
                 returnInfo = ReturnInfo()):
        """
        return hierarchical clustering of events into smaller clusters. 2-means clustering is applied on each node in the tree
        @param keywordCount: number of keywords to report in each of the clusters (at most 100)
        @param maxEventsToCluster: try to cluster at most this number of events (at most 10000)
        @param returnInfo: what details about the concepts should be included in the returned information
        """
        assert keywordCount <= 100
        assert maxEventsToCluster <= 10000
        self.resultType = "eventClusters"
        self.eventClustersKeywordCount = keywordCount
        self.eventClustersMaxEventsToCluster = maxEventsToCluster
        self.__dict__.update(returnInfo.getParams("eventClusters"))



class RequestEventsCategoryAggr(RequestEvents):
    def __init__(self,
                 returnInfo = ReturnInfo()):
        """
        return distribution of events into dmoz categories
        @param returnInfo: what details about the categories should be included in the returned information
        """
        self.resultType = "categoryAggr"
        self.__dict__.update(returnInfo.getParams("categoryAggr"))



class RequestEventsRecentActivity(RequestEvents):
    def __init__(self,
                 maxEventCount = 50,
                 updatesAfterTm = None,
                 updatesAfterMinsAgo = None,
                 mandatoryLocation = True,
                 lang = None,
                 minAvgCosSim = 0,
                 returnInfo = ReturnInfo()):
        """
        return a list of recently changed events that match search conditions
        @param maxEventCount: max events to return (at most 200)
        @param updatesAfterTm: the time after which the events were added/updated (returned by previous call to the same method)
        @param updatesAfterMinsAgo: how many minutes into the past should we check (set either this or updatesAfterTm property, but not both)
        @param mandatoryLocation: return only events that have a geographic location assigned to them
        @param lang: limit the results to events that are described in the selected language (None if not filtered by any language)
        @param minAvgCosSim: the minimum avg cos sim of the events to be returned (events with lower quality should not be included)
        @param returnInfo: what details should be included in the returned information
        """
        assert maxEventCount <= 2000
        assert updatesAfterTm == None or updatesAfterMinsAgo == None, "You should specify either updatesAfterTm or updatesAfterMinsAgo parameter, but not both"
        self.resultType = "recentActivityEvents"
        self.recentActivityEventsMaxEventCount = maxEventCount
        self.recentActivityEventsMandatoryLocation = mandatoryLocation
        if updatesAfterTm != None:
            self.recentActivityEventsUpdatesAfterTm = QueryParamsBase.encodeDateTime(updatesAfterTm)
        if updatesAfterMinsAgo != None:
            self.recentActivityEventsUpdatesAfterMinsAgo = updatesAfterMinsAgo
        if lang != None:
            self.recentActivityEventsLang = lang
        self.recentActivityEventsMinAvgCosSim = minAvgCosSim
        self.__dict__.update(returnInfo.getParams("recentActivityEvents"))


