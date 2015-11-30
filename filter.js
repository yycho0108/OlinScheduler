function collectCourseInfo(){
var record = [];

$("tr").each(function(){
var entry = $(this).children().filter("td");
if(entry.length == 12){
var content = [];

$(this).children().each(function(){
	var entryList = [];
	$(this).find("li").each(function(){ //if list
		entryList.push($(this).text());
	});
	if(entryList.length == 0){
		content.push($(this).text());
	}
	else{
		content.push(entryList);	
	}	
});

record.push({
	code : content[1],
	title : content[2],
	instructor : content[5], //list
	openSpots : content[6],
	status : content[7],
	meetingPattern : content[8], //list
	credit : content[9]
});
}});
console.log(record);
return record;
};

return collectCourseInfo();
