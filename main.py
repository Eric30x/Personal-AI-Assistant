from agent import run_agent, resume_agent
from agent import run_agent


def main():

    print("=== Personal AI Assistant ===")
    print("输入 exit 退出程序")

    while True:

        user_input = input("\n你：").strip()

        if user_input.lower() == "exit":
            print("助手已退出")
            break

        if not user_input:
            continue
        if user_input.lower() == "resume":

            try:
                answer = resume_agent()
                print("\nAI：", answer)

            except Exception as e:
                print(
                    f"恢复失败：{type(e).__name__}"
                )

            continue
        try:
            answer = run_agent(user_input)
            print("\nAI：", answer)

        except Exception as e:
            print(f"\n程序发生错误：{type(e).__name__}")
            print("本次请求可能未完成，请检查任务状态后再试。")


if __name__ == "__main__":
    main()
