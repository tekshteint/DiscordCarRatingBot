from bs4 import BeautifulSoup as bs
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import MongoDB_Client as db
import os
import aiohttp
import re
import datetime

class listingCrawler():
    def __init__(self, url):
        self.link = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.response = requests.get(self.link, headers=self.headers)
        self.filename = "outputHTML.xml"
        self.fbTitleFinal, self.fbDescFinal, self.fbPriceFinal, self.fbLocationFinal = None, None, None, None
        self.clTitleFinal, self.clDescFinal, self.clPriceFinal, self.clLocationFinal, self.clAttrFinal = None, None, None, None, {}
        self.linkType = None
        
        
        if "facebook" in self.link:
            self.crawlFB()
            
        elif "craigslist" in self.link:
            self.crawlCL()
            
        else:
            return
        
    def crawlFB(self):
        # Create the root element of the XML structure
        root = ET.Element("html")

        # Split the HTML source into lines
        html_lines = self.response.text.split('\n')

        # Create a parent element for the lines
        lines_element = ET.SubElement(root, "lines")

        # Iterate over the lines and create XML elements
        for line in html_lines:
            # Create an element for each line and append it to the parent element
            line_element = ET.SubElement(lines_element, "line")
            line_element.text = line

        # Create an ElementTree object with the root element
        tree = ET.ElementTree(root)

        # Convert the XML structure to a string
        xml_str = ET.tostring(root, encoding="utf-8")

        # Create a pretty-printed version of the XML string using minidom
        dom = minidom.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml(indent="    ")

        # Split the pretty-printed XML string by the "div" tag
        split_content = pretty_xml_str.split("div")

        # Join the split parts with a newline character
        new_content = "\n".join(split_content)

        # Write the modified content to a file
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(new_content)

        self.searchXML(self.filename)
        
        os.remove(self.filename)
        db.add_car_to_fb(str(self.getFBtitle()), self.getFBprice(), self.getFBlocation(), self.getFBdesc(),self.getLink())
            
    
    def crawlCL(self): 
        soup = bs(self.response.content, "html.parser")
        title = soup.find_all("span", {"id": "titletextonly"})
        price = soup.find_all("span", {"class": "price"})
        location = soup.find_all("meta", {"name": "geo.placename"})
        attributes = soup.find_all("div", {"class": "attrgroup"})
        attributesHTML = str(attributes[1])
        attributeSoup = bs(attributesHTML, "html.parser")
        spanElements = attributeSoup.find_all("span")
                
        classNames, values= [], []
        for span in spanElements:
            value, className = "",""
            if span.attrs["class"] == ['labl']:
                classNames.append(span.text.split(':')[0].strip())
            else:
                values.append(span.text.split(':')[0].strip())

        self.clAttrFinal = dict(zip(classNames, values))  
        
        description = soup.find_all("section", {"id" : "postingbody"})

        descList =[]
        for i in description:
            descList.append(i.text)
            i.next_sibling
        
        self.clDescFinal = [i for i in descList[0].split("\n") if i != ""]
        self.clDescFinal.pop(0)   
                
        self.clTitleFinal = str(title).replace('[<span id="titletextonly">', '').replace("</span>]", "")
        self.clPriceFinal = str(price).replace('[<span class="price">', '').replace("</span>]", "")
        self.clLocationFinal = str(location).replace('[<meta content="', '').replace('" name="geo.placename"/>]', '')
        
        db.add_car_to_cl(self.getCLtitle(), self.getCLprice(), self.getCLlocation(), self.getCLAttributes(), self.getCLdesc(), self.getLink())
        
    
    def searchXML(self, filename):
        with open(filename, 'r', encoding="utf8") as file:
            xml_text = file.read()
            
        lines = xml_text.splitlines()

        descSubstr = 'class=&quot;_59k _2rgt _1j-f _2rgt&quot; style=&quot;font-size: 14px;font-weight: 400;text-align: left&quot; id=&quot;'
        priceSubstr = 'class=&quot;_59k _2rgt _1j-f _2rgt _3zi4 _2rgt _1j-f _2rgt&quot; style=&quot;flex-grow:0;flex-shrink:0;'
        titleSubstr = 'class=&quot;_59k _2rgt _1j-f _2rgt _3zi4 _2rgt _1j-f _2rgt&quot; style=&quot;flex-grow:0;flex-shrink:1;margin:0 0 4px 0;'
        locationSubstr = 'class=&quot;_59k _2rgt _1j-f _2rgt _3zi4 _2rgt _1j-f _2rgt&quot; style=&quot;flex-grow:0;flex-shrink:1;margin:-4px 0 -5px 0;font-size: 15px;font-weight: 400;line-height: 20px;text-align: left;color:'
        
        descFinal = None
        priceFinal = None
        titleFinal = None
        locationFinal = None
        for line in lines:
            if descSubstr in line:
                descFinal = (line.split("&gt;"))
            elif priceSubstr in line:
                priceFinal = (line.split("&gt;"))
            elif titleSubstr in line:
                titleFinal = (line.split("&gt;"))
            elif locationSubstr in line:
                locationFinal = (line.split("&gt;"))
            else:
                pass
            
        if descFinal is not None: 
            descFinal.pop(0)
            strippedDesc = [s.replace("&lt;br /", "").strip("&lt;/") for s in descFinal]
            self.fbDescFinal = strippedDesc
            
        if priceFinal is not None: 
            self.fbPriceFinal = priceFinal[-1].replace("&lt;/", "")
        if titleFinal is not None: 
            self.fbTitleFinal = titleFinal[-1].replace("&lt;/", "")
        if locationFinal is not None: 
            self.fbLocationFinal = locationFinal[-1].replace("&lt;/", "").split("·")
            
    def printFBAttributes(self):
        print(self.fbTitleFinal)
        print(self.fbLocationFinal[0])
        print(self.fbPriceFinal)
        print("Description: ", end="")
        for line in self.fbDescFinal:
            print(line)
        
    def getFBtitle(self):
        if "·" in self.fbTitleFinal:
            self.fbTitleFinal = self.fbTitleFinal.split(" ·",)[0]
        return self.fbTitleFinal
    
    def getFBlocation(self):
        return self.fbLocationFinal[0]
    
    def getFBprice(self):
        return self.fbPriceFinal
    
    def getFBdesc(self):
        return self.fbDescFinal

    def printCLAttributes(self):
        print(self.clTitleFinal)
        print(self.clPriceFinal)
        print(self.clLocationFinal)
        for line in self.clAttrFinal:
            print(line, ":", self.clAttrFinal[line])
        print("Description: ", end="")
        for line in self.clDescFinal:
            print(line)

    def getCLtitle(self):
        return self.clTitleFinal
    
    def getCLlocation(self):
        return self.clLocationFinal
    
    def getCLprice(self):
        return self.clPriceFinal
    
    def getCLdesc(self): 
        return self.clDescFinal
    
    def getCLAttributes(self):
        return self.clAttrFinal

    def getLink(self):
        return self.link
    
    
async def determineLinkType(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            content_type = response.headers.get("content-type")

    if "facebook.com" in url:
        return "fb"
    elif "craigslist.org" in url:
        return "cl"
    else:
        return None


async def processListing(url):
    link_type = await determineLinkType(url)

    if link_type == "fb":
        crawler = listingCrawler(url)
    elif link_type == "cl":
        crawler = listingCrawler(url)
    else:
        print("Unsupported link type")
        
async def rateListing(url):
    rating = db.rateListing(url)
    return rating

async def rateModel(model):
    rating = db.rateModel(model)
    return f"{model} has an average price of ${rating}. Remember sometimes models don't have the right name because of how they're listed!"
    
    
""" async def tweak(model):
    rating = db.tweak(model)
    return rating """

async def returnDocument(model):
    rating = db.returnDocument(model)
    return rating

async def kbb(url):
    document = db.getDocument(url)
    
    """ Test Case """
    debug = False
    if debug:
        document = {
            "Make": "Mazda",
            "Model": "MX-5 Miata",
            "Year": 2006
        }
    
    kbbLinkBuilder = f"https://www.kbb.com/{document['Make'].lower()}/{document['Model'].replace(' ','-').lower()}/{document['Year']}/?condition=good&extcolor=black&intent=trade-in-sell&mileage={(datetime.datetime.now().year - document['Year']) * 15000}&modalview=false&offeroptions=true&options=6461370%7ctrue&pricetype=private-party&subintent=sell"    
    print(kbbLinkBuilder)
    soup = bs(requests.get(kbbLinkBuilder).content, "html.parser")
    objects = soup.find("object")
    
    script_tag = soup.find('script', text=lambda text: text and 'window.__APOLLO_STATE__' in text)

    # Extract the content inside the script tag
    script_content = script_tag.string
    vehicleIdMatch = r'"vehicleId":"(.*?)"'
    matches = re.findall(vehicleIdMatch, str(script_content))
    
    vehicleId = matches[0]
 
    """ soup = bs(requests.get(kbbLinkBuilder).content, "html.parser")
    objects = soup.find("object")
    newCall = objects.get('data')
    cleanedCall = re.sub(r'&amp;', '', newCall)
    print(cleanedCall)
    
    #return cleanedCall
    kbbResponse = requests.get(cleanedCall)
    return kbbResponse.content"""
    upaStringBuilder = f"https://upa.syndication.kbb.com/usedcar/privateparty/sell/?apikey=76a9532b-fa54-4d02-8e6a-91c3fb85376c&zipcode=90801&vehicleid={vehicleId}&condition=good&mileage=206000&format=svg"
    kbbSVG = requests.get(upaStringBuilder)
    with open("Bot/kbbSVG.svg", "wb") as file:
        file.write(kbbSVG.content)
        
    return 200
    

    
if __name__ == "__main__":

    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/849146070311769/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks")
    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/1527363641422998/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks")
    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/1375343499699020/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks")
    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/688893393165373/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks")
    #print(type(fbTest.getFBdesc()))
    #print(type(fbTest.getFBlocation()))
    #print(type(fbTest.getFBprice()))
    #print(type(fbTest.getFBtitle()))

    #db.add_car_to_fb(fbTest.getFBtitle(), fbTest.getFBprice(), fbTest.getFBlocation(), fbTest.getFBdesc(),fbTest.getLink())
    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/574244454853965/")
    #db.add_car_to_fb(fbTest.getFBtitle(), fbTest.getFBprice(), fbTest.getFBlocation(), fbTest.getFBdesc(),fbTest.getLink())
    #fbTest = listingCrawler("https://www.facebook.com/marketplace/item/722548419671590/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks")
    #db.add_car_to_fb(fbTest.getFBtitle(), fbTest.getFBprice(), fbTest.getFBlocation(), fbTest.getFBdesc(),fbTest.getLink())
    #fbTest.printFBAttributes()

    #clTest = listingCrawler("https://sfbay.craigslist.org/nby/cto/d/santa-rosa-2002-mercedes-class-wagon/7637474868.html")
    #db.add_car_to_cl(clTest.getCLtitle(), clTest.getCLprice(), clTest.getCLlocation(), clTest.getCLAttributes(), clTest.getCLdesc(),clTest.getLink())
    #clTest = listingCrawler("https://sfbay.craigslist.org/eby/cto/d/fairfield-1977-ford-thunderbird/7637474855.html")
    #db.add_car_to_cl(clTest.getCLtitle(), clTest.getCLprice(), clTest.getCLlocation(), clTest.getCLAttributes(), clTest.getCLdesc(),clTest.getLink())
    #clTest = listingCrawler("https://sfbay.craigslist.org/eby/cto/d/fremont-2015-audi-a3-18t-prestige-clean/7637474621.html")
    #db.add_car_to_cl(clTest.getCLtitle(), clTest.getCLprice(), clTest.getCLlocation(), clTest.getCLAttributes(), clTest.getCLdesc(),clTest.getLink())
    #clTest = listingCrawler("https://sfbay.craigslist.org/eby/cto/d/emeryville-2013-mini-countryman-jcw-all4/7637511070.html")
    #db.add_car_to_cl(clTest.getCLtitle(), clTest.getCLprice(), clTest.getCLlocation(), clTest.getCLAttributes(), clTest.getCLdesc(),clTest.getLink())
    #clTest.printCLAttributes()
    #print(clTest.getCLtitle())

    #db.add_car_to_cl(clTest.getCLtitle(), clTest.getCLprice(), clTest.getCLlocation(), clTest.getCLAttributes(), clTest.getCLdesc())

    #db.add_car_to_fb(fbTest.getFBtitle(), fbTest.getFBprice(), fbTest.getFBlocation(), fbTest.getFBdesc())
    #rate = db.rateListing("https://www.facebook.com/marketplace/item/179647175179591/?referralSurface=messenger_lightspeed_banner&referralCode=messenger_banner")
    #clTest = listingCrawler("https://losangeles.craigslist.org/lac/cto/d/los-angeles-1994-mazda-miata-na-manual/7727862632.html")
    
    #url = "https://www.kbb.com/mazda/mx-5-miata/2006/club-spec-convertible-2d/?condition=good&extcolor=blue&intent=trade-in-sell&mileage=206000&modalview=false&offeroptions=true&options=6461370%7ctrue&pricetype=private-party&subintent=sell"
    url = "https://www.facebook.com/marketplace/item/774603191045694/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks"
    kbb(url)
    
    