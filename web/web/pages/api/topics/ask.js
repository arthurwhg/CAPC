import {askTopic} from "../../../services/llmService/topicask"

export default async function ask(req, res) {
    const {question} = req.body;
    //console.log(question)
    const answer = await askTopic(question);
    //console.log(answer)
    if (typeof(answer) !== 'undefined') {
      res.status(200).json(answer);
    } else {
      res.status()
    }
  }