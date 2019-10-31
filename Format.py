class Format:
    # this class is used to manipulate text,and URLs into common formats

    def removeRedundantSpaces(str):
        # removes all instances of multiple spaces
        return " ".join(str.split())

    def convertToAbsoluteURL(domain,url):
        # converts relative URLs to absolute URLs
        # if the URL is already absolute, no changes would be applied.
        if "//www." not in url:
            return domain[0:-1] + url  # join the domain without the last /
        return url

    def convertToAplhanumeric(str):
        # returns a new string in which each character is either a character, a number or a space.
        return ''.join(c for c in str if c.isalnum() or c == ' ')
