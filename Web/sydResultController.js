const nano = require("nano")("http://admin:170645@172.26.131.170:5984")
// change the profile details
const sydResult = async (req, res) => {
    var db = nano.use('twitter_sentiment_syd')
    var total = []
    try{
        await db.view('sentiment_analysis','count_sentiment',{group: true}).then((body) => {
            body.rows.forEach((result) => {
                //console.log(result);
                total.push(result)
            });
        });
        //return res.send(total)
        return res.render('syd_index',{layout:'main',"thisResult":total})
    } catch (err){
        res.status(400)
        console.log(err)
        return res.send("Internal Error")
    }

}

module.exports = {
    sydResult
}