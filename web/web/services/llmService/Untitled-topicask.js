import { askTopic } from './topicask'; // Assuming topicask.js is in the same directory

// Mock the fetch function
global.fetch = jest.fn();

describe('askTopic', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('should successfully fetch and return data on a 200 response', async () => {
    const mockResponse = {
        hits: [{ id: 1, name: 'Topic 1' }, { id: 2, name: 'Topic 2' }],
        // Add other properties if needed according to the expected structure
    };

    fetch.mockResolvedValueOnce({
      status: 200,
      json: () => Promise.resolve(mockResponse),
    });

    const question = 'What is the meaning of life?';
    const result = await askTopic(question);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });
    expect(result).toEqual(mockResponse.hits);
  });

  it('should handle non-200 responses and return null', async () => {
    fetch.mockResolvedValueOnce({
      status: 404,
    });

    const question = 'Another question';
    const result = await askTopic(question);

    expect(fetch).toHaveBeenCalledTimes(1);
     expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });
    expect(result).toBeNull();
  });

  it('should handle fetch errors and return null', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      const question = 'A difficult question';
      const result = await askTopic(question);
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });
      expect(result).toBeNull();
    });
   it('should handle empty json response', async () => {
        const mockResponse = {}
        fetch.mockResolvedValueOnce({
            status: 200,
            json: () => Promise.resolve(mockResponse),
        });

        const question = 'What is the meaning of life?';
        const result = await askTopic(question);

        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              question: question,
            }),
        });
        expect(result).toBeUndefined();

   });
    it('should send the correct question in the request body', async () => {
        const mockResponse = { hits: [] }; 
        fetch.mockResolvedValueOnce({
            status: 200,
            json: () => Promise.resolve(mockResponse),
        });

        const question = 'Test Question';
        await askTopic(question);

        expect(fetch).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
            body: JSON.stringify({ question: question }),
        }));
    });

     it('should handle a 500 Internal Server Error', async () => {
        fetch.mockResolvedValueOnce({
            status: 500,
        });

        const question = 'Test question causing an error';
        const result = await askTopic(question);

        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', expect.anything());
        expect(result).toBeNull();
    });
    it('should handle a JSON parse error', async () => {
        // Simulate a response that can't be parsed as JSON
        fetch.mockResolvedValueOnce({
            status: 200,
            json: () => Promise.reject(new Error("Unexpected token < in JSON at position 0")),
        });

        const question = "What's wrong?";
        const result = await askTopic(question);

        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('localhost:8000/llm/api/v1/topicanswer/question/', expect.anything());
        expect(result).toBeNull();
    });

});
