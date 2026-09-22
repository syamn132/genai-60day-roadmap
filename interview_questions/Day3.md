1. What is the purpose of the loss function in LLM training?
A. The loss function measures how far the model’s predicted probability distribution is from the correct next-token target. In language modeling, cross-entropy loss penalizes the model when it assigns low probability to the true token. The resulting loss is then used by backpropagation to compute gradients for updating the model’s parameters.


2. What is fine-tuning?
A. Fine-tuning is the process of taking a pretrained model and continuing its training on a smaller task- or domain-specific dataset so that its behavior becomes better suited to a particular use case.

3. What is instruction tuning?
A. Instruction tuning is a form of fine-tuning where the model is trained on instruction-response examples so that it becomes better at following human instructions.

4. Fine-tuning vs RAG?
A. Fine-tuning primarily changes the model's behavior by updating parameters, while RAG retrieves external information at inference time without requiring that knowledge to be encoded into the model weights.