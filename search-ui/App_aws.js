import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields
} from "./config/config-helper";

const connector = new ElasticsearchAPIConnector({
  host: "http://es01:9200",
  index: "cv-transcriptions",
});

// Testing the connection
fetch(connector.host)
  .then((response) => {
    if (response.ok) {
      console.log("Successfully connected to Elasticsearch!");
    } else {
      console.error("Failed to connect to Elasticsearch. Status code:", response.status);
    }
  })
  .catch((error) => {
    console.error("Error connecting to Elasticsearch:", error.message);
  });

const config = {
  searchQuery: {
    search_fields: {
      generated_text: {
        weight: 3
      },
      // duration: {},
      age: {},
      gender: {},
      accent: {}
    },
    result_fields: {
      generated_text: {
        snippet: {}
      },
      duration: {
        snippet: {}
      },
      age: {
        snippet: {}
      },
      gender: {
        snippet: {}
      },
      accent: {
        snippet: {}
      },
      // filename: {
      //   snippet: {}
      // }
    },
    disjunctiveFacets: ["gender.keyword", "accent.keyword"],
    facets: {
      "gender.keyword": { type: "value" },
      "accent.keyword": { type: "value" },
      "age.keyword": {
        type: "value", // Change type to "value" for keyword-style search
        size: 10, // Set the number of displayed values in the facet
      },
      duration: {
        type: "range",
        ranges: [
          { from: 0, to: 5, name: "0 - 5 seconds" },
          { from: 5, to: 10, name: "5 - 10 seconds" },
          { from: 10, to: 15, name: "10 - 15 seconds" },
          { from: 15, to: 20, name: "15 - 20 seconds" },
          { from: 20, to: 25, name: "20 - 25 seconds" },
          { from: 25, to: 30, name: "25 - 30 seconds" },
          { from: 30, to: 2592000, name: ">30 seconds" }
        ]
      }
    }
  },
  autocompleteQuery: {
    results: {
      resultsPerPage: 5, 
      search_fields: {
        "generated_text.suggest": {
          weight: 3
        }
      },
      result_fields: {
        generated_text: {
          snippet: {
            size: 100,
            fallback: true
          }
        }
      }
    },
    suggestions: {
      types: {
        results: { fields: ["generated_text.suggest"] }
      },
      size: 4
    }
  }, 
  apiConnector: connector, 
  alwaysSearchOnInitialLoad: true
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox  />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort by"}
                          sortOptions={buildSortOptionsFromConfig()}
                        />
                      )}
                      {getFacetFields().map((field) => (
                        <Facet key={field} field={field} label={field} />
                      ))}
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      urlField={getConfig().urlField}
                      thumbnailField={getConfig().thumbnailField}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
