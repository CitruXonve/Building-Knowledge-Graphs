// Step #1, import Statements
import React from "react";
import queryString from 'query-string';
import { useHistory } from "react-router-dom";
import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";
import { SearchProvider, Results, SearchBox } from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import {
    PagingInfo,
    ResultsPerPage,
    Paging,
    Facet,
    Sorting,
    ErrorBoundary
} from "@elastic/react-search-ui";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import $ from 'jquery';
// Step #2, The Connector
const connector = new AppSearchAPIConnector({
    searchKey: "search-weg5x9xous972kvpsjr7ncbc",
    // apiKey: "private-ows57c91xh1og2y6ozese9ne",
    engineName: "inf558",
    endpointBase: "http://localhost:3002"
});
// Step #3: Configuration Options
const configurationOptions = {
    apiConnector: connector,
    // Let's fill this in together.
    alwaysSearchOnInitialLoad: true,
    initialState: {
        resultsPerPage: 5
    },
    searchQuery: {
        search_fields: {
            title: {},
            label: {},
            // description: {},
            // url: {},
        },
        result_fields: {
            title: {
                snippet: {
                    size: 100,
                    fallback: true,
                },
            },
            description: {
                snippet: {
                    size: 100,
                    fallback: true,
                },
            },
            url: {
                raw: {},
            },

            label: {
                raw: {},
            },
        },
        facets: {
            title: {
                type: "value",
                size: 50,
            },
            description: {
                type: "value",
                size: 200,
            },
            url: {
                type: "value",
                size: 80,
            },
            type: {
                type: "value",
            }
        },
    },
    autocompleteQuery: {
        results: {
            resultsPerPage: 8,
        },
        suggestions: {
            types: {
                documents: {
                    // Which fields to search for suggestions.
                    fields: ["title", "description", "label"]
                },
            },
            // How many suggestions appear.
            size: 10,
        }
    },
};
// Step #4, SearchProvider: The Finishing Touches.
export default class Search extends React.Component{
    constructor(props){
        super(props)
        this.state={

        }
    }

    handleClick = (event) => {
        event.preventDefault();
        var target = $(event.target);
        if (target.is("a") || target.is("em")) {
            var item = target.parents("li");
            var id = item.html().replace(/<[^>]+>/g, " ").match(/id\s*([a-z0-9\-]+)/g)[0].replace(/id\s*/, '')
            console.log(id);
            this.props.onResultClick(id);

            // const history = useHistory();
        }
    }

    componentDidMount = () => {
        // alert()
    }

    render = () => (
        <SearchProvider config={configurationOptions}>
            <div className="App">
                <Layout
                    // Let's fill this in together.
                    header={<SearchBox autocompleteSuggestions={true} />}
                    // titleField is the most prominent field within a result: the result header.
                    bodyContent={<Results titleField="title" urlField="url" shouldTrackClickThrough={true} onClick={this.handleClick} />}
                    sideContent={
                        <div>
                            <Sorting
                                label={"Sort by"}
                                sortOptions={[
                                    {
                                        name: "Relevance",
                                        value: "",
                                        direction: ""
                                    },
                                    {
                                        name: "Title",
                                        value: "title",
                                        direction: "asc"
                                    }
                                ]}
                            />
                            <Facet field="type" label="Type" isFilterable={true} />
                            {/* <Facet field="label" label="Label"/> */}
                        </div>
                    }
                    bodyHeader={
                        <>
                            <PagingInfo />
                            <ResultsPerPage options={[5, 10, 15]} />
                        </>
                    }
                    bodyFooter={<Paging />}
                />
            </div>
        </SearchProvider>
    );
}