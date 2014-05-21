from portality import pyoag
import csv, codecs

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="source csv to read identifiers from")
    parser.add_argument("-o", "--out", help="output csv to write results to")
    parser.add_argument("-e", "--error", help="output csv to write errors to")

    args = parser.parse_args()

    if not args.source:
        print "Please specify a source with the -u option"
        exit()

    if not args.out:
        print "Please specify an output file with the -o option"
        exit()

    if not args.error:
        print "Please specify an error output file with the -e option"
        exit()

    # read in the identifiers
    identifiers = []
    with open(args.source) as source:
        reader = csv.reader(source)
        for row in reader:
            identifiers.append(row[0])

    print "resolving ", len(identifiers), "identifiers"

    req = pyoag.Request(query=identifiers, timeoutdelay=500)

    # <th>identifier</th><th>license</th><th>BY</th><th>NC</th><th>SA</th><th>ND</th><th>OKD</th><th>OSI</th><th>info</th><th>checked</th><th>by</th>

    #var info = '<p>' + record.license[0].provenance.description + '</p>';
    #        if (record.license[0].url) {
    #            info += '<p>Learn more about this license at <a target="_blank" href="' + record.license[0].url + '">' + record.license[0].url + '</a></p>'
    #        }
    #        if (record.license[0].provenance.source) {
    #            info += '<p>We retrieved this information from <a target="_blank" href="' + record.license[0].provenance.source + '">' + record.license[0].provenance.source + '</a>.</p>';
    #        }

    # record.license[0].provenance.handler + '">' + record.license[0].provenance.handler_version

    #row += "<td" + color + ">" + record.license[0].title + " (" + record.license[0].type + ")</td>"
    #        row += "<td>" + record.license[0].BY + "</td>"
    #        row += "<td>" + record.license[0].NC + "</td>"
    #        row += "<td>" + record.license[0].SA + "</td>"
    #        row += "<td>" + record.license[0].ND + "</td>"
    #        row += "<td>" + (typeof(record.license[0].is_okd_compliant) === "undefined" ? "" : record.license[0].is_okd_compliant) + "</td>"
    #        row += "<td>" + (typeof(record.license[0].is_osi_compliant) === "undefined" ? "" : record.license[0].is_osi_compliant) + "</td>"
    #        row += "<td>" + info + "</td>"
    #        row += "<td>" + record.license[0].provenance.date + "</td>"
    #        row += "<td>" + plugin + "</td>"
    #        row += "</tr>"
    with codecs.open(args.out, "wb") as output:
        writer = csv.writer(output)
        writer.writerow(["identifier", "license title", "license type", "license url", "by", "nc", "sa", "nd", "okd compliant", "osi compliant", "info", "source", "checked", "plugin"])
        for res in req.response:
            identifier = res.get("identifier", [{}])[0].get("id")
            ltitle = res.get("license", [{}])[0].get("title")
            ltype = res.get("license", [{}])[0].get("type")
            by = res.get("license", [{}])[0].get("by")
            nc = res.get("license", [{}])[0].get("nc")
            sa = res.get("license", [{}])[0].get("sa")
            nd = res.get("license", [{}])[0].get("nd")
            okd = res.get("license", [{}])[0].get("is_okd_compliant")
            osi = res.get("license", [{}])[0].get("is_osi_compliant")
            checked = res.get("license", [{}])[0].get("provenance", {}).get("date")
            info = res.get("license", [{}])[0].get("provenance", {}).get("description")
            license_url = res.get("license", [{}])[0].get("url")
            source = res.get("license", [{}])[0].get("provenance", {}).get("source")
            plugin = res.get("license", [{}])[0].get("provenance", {}).get("handler") + " " + res.get("license", [{}])[0].get("provenance", {}).get("handler_version")

            csv_row = [identifier, ltitle, ltype, license_url, by, nc, sa, nd, okd, osi, info, source, checked, plugin]
            clean_row = [unicode(c).encode("utf8", "replace") if c is not None else "" for c in csv_row]
            writer.writerow(clean_row)

    with codecs.open(args.error, "wb") as eout:
        ewriter = csv.writer(eout)
        ewriter.writerow(["identifier", "error"])
        for err in req.errors:
            identifier = err.get("identifier", [{}]).get("id")
            msg = err.get("error")

            csv_row = [identifier, msg]
            clean_row = [unicode(c).encode("utf8", "replace") if c is not None else "" for c in csv_row]
            ewriter.writerow(clean_row)



