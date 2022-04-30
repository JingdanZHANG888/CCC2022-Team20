// change the profile details
const wordCloud = async (req, res) => {
   
    try{
        console.log('11')
        return res.render('wordCloud',{layout:'main'})
    } catch (err){
        res.status(400)
        console.log(err)
        return res.send("Internal Error")
    }

}

module.exports = {
    wordCloud
}