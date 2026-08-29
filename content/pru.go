package main

import "fmt"
import "net/http"

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        if r.FormValue("q") != "" {
            fmt.Fprintf(w, `
                <body>
                    <h1>Hello, %s</h1>
                </body>
            `, r.FormValue("q"))
            return
        }
        fmt.Fprintf(w, `
            <body>
                <form action="/" method="GET">
                    <label>Enter your name</label>
                    <input name="q">
                    <button type="submit">Submit</button>
                </form>
            </body>
        `)
    })

    http.ListenAndServe(":8080", nil)
}
