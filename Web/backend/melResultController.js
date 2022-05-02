const nano = require("nano")("http://admin:170645@172.26.131.170:5984")
// change the profile details
const melResult = async (req, res) => {
    var db = nano.use('twitter_sentiment')
    var total = []
    var count = 0
    try{
        await db.view('sentiment_analysis','count_sentiment',{group: true}).then((body) => {
            body.rows.forEach((result) => {
                count += result.value
                
            });
            body.rows.forEach((result) => {
                result["percentage"] = (result.value/count*100).toFixed(2)
                total.push(result)
            });
        });
        //return res.send(total)
        return res.render('../../frontend/views/index',{layout:'../../../frontend/views/layouts/main',"thisResult":total})
    } catch (err){
        res.status(400)
        console.log(err)
        return res.send("Internal Error")
    }

}

module.exports = {
    melResult
}