# Tử Vi Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành trong hệ thống Tử Vi Đẩu Số, một trong những bộ môn kinh điển của phong thủy và tử vi học Đông Á. Tử Vi là hệ thống số học phức tạp sử dụng các cung, sao, và vòng tròn tử vi để phân tích vận mệnh con người. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh ứng dụng trong thực tế và cách implement trong hệ thống.

## Các thuật ngữ cơ bản

### 1. Đẩu Số (斗數 - Dou Shu)

Đẩu Số là tên gọi đầy đủ của hệ thống Tử Vi, bao gồm "Tử Vi Đẩu Số" - nghĩa là hệ thống đếm số của Tử Vi. Đẩu Số sử dụng các vòng tròn tử vi, cung điền, và sự sắp xếp của các sao trong mỗi cung để phân tích vận mệnh. Khác với Bazi (Bát Tự) dựa trên ngày giờ sinh, Đẩu Số dựa trên giờ sinh để xác định cung Mệnh và phân bổ các sao vào các cung trong lá số.

Hệ thống Đẩu Số bao gồm nhiều vòng tròn: Tử Vi, Lương Hổ, Tứ Hóa, Sát Phá, và nhiều vòng khác. Mỗi vòng tròn mang một ý nghĩa riêng và contributes vào bức tranh tổng thể của lá số. Trong lập trình, Đẩu Số được biểu diễn như một complex data structure với nested objects cho các vòng tròn và các sao trong mỗi vòng.

### 2. Cung (宮 - Palace)

Cung là các vị trí trong lá số Tử Vi, tương ứng với các khía cạnh khác nhau của cuộc đời. Có 12 cung chính trong Tử Vi: Mệnh, Phụ Mẫu, Huynh Đệ, Thiên Di, Tài Bạch, Tướng Phú, Nô Bộc, Thân, Phu Thê, Tử Tức, Phúc Đức, và Điền Trạch. Mỗi cung mang một ý nghĩa riêng và chứa các sao với mức độ ảnh hưởng khác nhau.

Cung Mệnh (命宮) là cung quan trọng nhất, đại diện cho bản thân người sinh, tính cách, và vận mệnh tổng quát. Cung Phụ Mẫu (父母宮) liên quan đến cha mẹ, tổ tiên, và người giám hộ. Cung Thân (身宮) thể hiện thể xác, sức khỏe, và cách người khác nhìn nhận. Việc xác định chính xác các cung dựa trên giờ sinh là nền tảng của mọi phân tích Tử Vi.

### 3. Sao (星 - Star)

Sao là các ngôi sao được đặt vào các cung trong lá số Tử Vi. Có nhiều loại sao với ý nghĩa và cấp bậc khác nhau. Sao chính (主星) gồm: Tử Vi, Lưỡng Kim, Điền Trạch, Quan Phủ, Nhật, Nguyệt, Tấn, Xương, Cuồng, và các sao khác. Sao phụ (Phụ Tinh) gồm các sao có tác dụng bổ trợ hoặc giảm nhẹ tác động của sao chính.

Sao Tử Vi (紫微星) là sao chính quan trọng nhất, đại diện cho hoàng đế, quyền uy, và địa vị xã hội. Sao Nguyệt (Nguyệt Đức) mang năng lượng âm, đại diện cho mẹ, tài chính, và sự mềm mại. Sao Nhật (Nhật Đức) mang năng lượng dương, đại diện cho cha, danh dự, và sự năng động. Mỗi sao có các tính chất riêng và tương tác với các sao khác trong cùng cung và các cung liền kề.

### 4. Vòng Tròn Tử Vi (紫微斗數 - Zi Wei Dou Shu Cycle)

Vòng Tròn Tử Vi là hệ thống phân bổ các sao vào 12 cung dựa trên giờ sinh và giới tính. Có 12 vòng tròn chính: Tử Vi, Lương Hổ, Tứ Hóa, Sát Phá, Bác Sát, Hóa Lộc, Hóa Quyền, Hóa Khoa, Tài Bạch, Quan Phủ, và các vòng khác. Mỗi vòng tròn có quy tắc phân bổ riêng và mang một khía cạnh ý nghĩa khác nhau.

Vòng tròn Tử Vi là vòng tròn cơ bản nhất, xác định vị trí của Tử Vi và các sao chính theo giờ sinh. Vòng Lương Hổ xác định Lương và Hổ, hai sao quan trọng về tài lộc. Vòng Tứ Hóa gồm Hóa Lộc, Hóa Quyền, Hóa Khoa, Hóa Lưu mang ý nghĩa về sự biến đổi và phát triển. Trong hệ thống, mỗi vòng tròn được implement như một function nhận inputs và trả về mapping của sao vào các cung.

### 5. Thập Nhị Cung (十二宮 - Twelve Palaces)

Thập Nhị Cung là 12 cung trong lá số Tử Vi, mỗi cung có một tên gọi và ý nghĩa riêng. Cung Mệnh (命宮) đại diện cho bản thân, tính cách, và vận mệnh. Cung Phụ Mẫu (父母宮) liên quan đến cha mẹ, công việc, và học vấn gốc. Cung Huynh Đệ (兄弟宮) thể hiện mối quan hệ với anh chị em và bạn bè. Cung Thiên Di (田宅宮) liên quan đến nhà cửa, gia đình, và tổ tiên.

Cung Tài Bạch (財帛宮) đại diện cho tài chính, thu nhập, và cách kiếm tiền. Cung Tướng Phú (官祿宮) liên quan đến sự nghiệp, công việc, và địa vị xã hội. Cung Nô Bộc (僕僕宮) thể hiện mối quan hệ với người giúp việc,subordinates, và enemies. Cung Thân (身宮) đại diện cho thể xác, sức khỏe, và cách người khác nhìn nhận. Cung Phu Thê (夫妻宮) liên quan đến hôn nhân và mối quan hệ tình cảm.

### 6. Cung Mệnh và Cung Thân (命宮 - Life Palace, 身宮 - Body Palace)

Cung Mệnh là cung quan trọng nhất trong lá số Tử Vi, nằm ở vị trí được xác định dựa trên giờ sinh và giới tính. Cung Mệnh đại diện cho bản thân người sinh, tính cách, ngoại hình, và xu hướng vận mệnh tổng quát. Các sao trong Cung Mệnh ảnh hưởng lớn đến cách đọc lá số. Người có Cung Mệnh tốt thường có cuộc sống ổn định và thuận lợi.

Cung Thân thường nằm đối diện hoặc gần Cung Mệnh, đại diện cho thể xác, sức khỏe, và cách người khác nhìn nhận về bạn. Cung Thân cũng liên quan đến cách bạn thể hiện bản thân ra bên ngoài. Trong một số trường hợp, Cung Thân được coi là quan trọng hơn Cung Mệnh vì nó thể hiện "hình dạng" thực tế của cuộc đời. Khi Cung Mệnh và Cung Thân đều tốt, người đó thường có cuộc sống viên mãn.

### 7. Vòng Lương Hổ (糧糊宮 - Wealth Tiger Cycle)

Vòng Lương Hổ là vòng tròn quan trọng trong Tử Vi, xác định vị trí của Lương và Hổ trong lá số. Lương Tinh (粮星) đại diện cho tài lộc, tiền bạc, và sự sung túc. Hổ Tinh (虎星) đại diện cho sự mạnh mẽ, quyền lực, và khả năng lãnh đạo. Hai sao này thường được xem xét cùng nhau để đánh giá vận tài và địa vị.

Lương Hổ cũng liên quan đến sự nghiệp và cơ hội trong cuộc đời. Khi Lương và Hổ đều ở các cung tốt, người đó thường có tài lộc và địa vị tốt. Ngược lại, khi Lương Hổ ở các cung xấu hoặc bị các sao xấu chiếu, có thể gặp khó khăn về tài chính hoặc sự nghiệp. Trong hệ thống, vòng Lương Hổ được implement như một function nhận giờ sinh và giới tính, trả về vị trí của hai sao này.

### 8. Vòng Tứ Hóa (四化星 - Four Transformations Cycle)

Vòng Tứ Hóa là vòng tròn quan trọng trong Tử Vi, bao gồm bốn sao biến đổi: Hóa Lộc, Hóa Quyền, Hóa Khoa, và Hóa Lưu. Mỗi sao Hóa mang ý nghĩa về sự biến đổi và phát triển trong một khía cạnh cụ thể của cuộc sống. Vòng Tứ Hóa giúp xác định những điểm mạnh và điểm yếu, cơ hội và thách thức trong cuộc đời.

Hóa Lộc (化祿) đại diện cho sự sung túc, may mắn về tài chính, và cơ hội. Hóa Quyền (化權) thể hiện quyền lực, khả năng lãnh đạo, và ý chí mạnh mẽ. Hóa Khoa (化科) liên quan đến học vấn, danh tiếng, và sự nổi tiếng. Hóa Lưu (化流) đại diện cho sự lưu chuyển, thay đổi, và chuyển động. Vị trí của các sao Hóa trong lá số cho biết những lĩnh vực nào sẽ có sự phát triển và biến đổi.

### 9. Sát Phá (煞星 - Sha Stars)

Sát Phá là nhóm các sao xấu trong Tử Vi, bao gồm: Sát, Phá, Lưu, và Triệt. Các sao này mang năng lượng xung đột, khó khăn, và thách thức. Khi xuất hiện trong các cung quan trọng, chúng có thể gây ra những trở ngại và biến cố trong cuộc sống. Tuy nhiên, Sát Phá không phải lúc nào cũng xấu; chúng có thể tạo động lực để vượt qua khó khăn và phát triển bản thân.

Sát Tinh (煞星) đại diện cho sự xung đột, cạnh tranh, và thử thách. Phá Tinh (破星) thể hiện sự phá hủy, thay đổi, và tái cấu trúc. Lưu Tinh (流星) liên quan đến thời gian và sự lưu chuyển. Triệt Tinh (迭星) đại diện cho sự gián đoạn và trì hoãn. Trong phân tích, Sát Phá cần được xem xét cùng với các sao tốt và xấu khác trong cùng cung để đưa ra đánh giá toàn diện.

### 10. Các Sao Phụ (輔星 - Auxiliary Stars)

Các Sao Phụ là nhóm các sao bổ trợ trong Tử Vi, bao gồm: Tấn, Xương, Cuồng, Đà, Sảnh, Hợp, và nhiều sao khác. Các sao này không có ảnh hưởng quyết định như sao chính nhưng có tác dụng bổ trợ, tăng cường hoặc giảm nhẹ tác động của sao chính trong cùng cung. Chúng tạo ra những sắc thái khác nhau trong ý nghĩa của mỗi cung.

Tấn (進星) và Xương (昌星) thường được xem cùng nhau, mang ý nghĩa về sự thịnh vượng và phát triển. Cuồng (狂星) có thể gây ra sự bất ổn và cần được xem xét cẩn thận. Đà (陀星) và Sảnh (祿星) tạo thành cặp Đà Sảnh, liên quan đến sự chậm trễ và may mắn. Hợp (合星) đại diện cho sự hài hòa và hợp tác. Việc đọc lá số cần xem xét cả sao chính và sao phụ để có bức tranh đầy đủ.

### 11. Liên Cung (連宮 - Connected Palaces)

Liên Cung là mối quan hệ giữa các cung trong lá số Tử Vi, thể hiện sự kết nối và ảnh hưởng qua lại giữa các khía cạnh cuộc sống. Có nhiều loại liên cung: Song Cung (đối diện), Tam Hợp (ba cung hợp nhau), và Tứ Hành Xung (bốn cung xung nhau). Liên cung giúp xác định cách một cung ảnh hưởng đến các cung khác và ngược lại.

Song Cung là hai cung đối diện nhau trong vòng tròn 12 cung. Ví dụ Mệnh và Phu Thê là Song Cung, Thân và Tài Bạch là Song Cung. Khi một cung tốt, Song Cung của nó cũng được hưởng lợi. Tam Hợp là nhóm ba cung có mối quan hệ hài hòa: Mệnh-Thiên Di-Tài Bạch, Phụ Mẫu-Huynh Đệ-Nô Bộc, và các nhóm khác. Tứ Hành Xung là bốn cung xung nhau tạo thành hình vuông, mang năng lượng xung đột và cần được xem xét cẩn thận.

### 12. Minh Cung và Án Cung (明宮暗宮 - Bright and Dark Palaces)

Minh Cung là các cung được chiếu sáng bởi sao tốt hoặc ánh sáng từ các sao chính, thể hiện sự thịnh vượng và thuận lợi. Án Cung là các cung ở trong bóng tối hoặc bị các sao xấu chiếu, thể hiện khó khăn và thách thức. Việc xác định Minh Cung và Án Cung giúp hiểu rõ hơn về sự phân bố năng lượng trong lá số.

Án Cung không phải lúc nào cũng xấu; trong một số trường hợp, Án Cung có thể mang ý nghĩa về sự ẩn dấu, bí mật, hoặc những nguồn lực tiềm ẩn. Tuy nhiên, khi Án Cung chứa nhiều sao xấu, nó thường mang lại những thách thức lớn hơn. Trong hệ thống, việc xác định Minh/Án Cung dựa trên vị trí của Tử Vi, Nguyệt, Nhật và các sao ánh sáng khác.

### 13. Vận (運 - Fortune Period)

Vận trong Tử Vi là các giai đoạn thời gian được phân chia theo năm hoặc thập niên, thể hiện sự thay đổi của vận mệnh theo thời gian. Mỗi người trải qua nhiều Vận khác nhau trong đời, mỗi Vận kéo dài một số năm và mang những đặc điểm riêng. Vận được xác định dựa trên giờ sinh và giới tính, chia lá số thành các giai đoạn với các sao chủ đạo khác nhau.

Vận Niên (年運) là vận của từng năm, cho biết xu hướng và cơ hội trong năm đó. Vận Thập Niên (十年運) là vận của mỗi 10 năm, thể hiện những thay đổi lớn hơn trong cuộc đời. Khi đọc Vận, cần xem xét các sao trong cung Vận hiện tại và mối quan hệ với Cung Mệnh. Vận tốt thường mang lại thuận lợi và phát triển; Vận xấu cần cẩn thận và chuẩn bị để vượt qua thách thức.

### 14. Đại Vận và Tiểu Vận (大運小運 - Major and Minor Fortune)

Đại Vận là giai đoạn vận dài hơn trong Tử Vi, thường kéo dài 10 năm hoặc theo một quy luật riêng dựa trên giờ sinh. Đại Vận cho biết xu hướng tổng thể của một giai đoạn dài trong cuộc đời, thường được dùng để lập kế hoạch dài hạn. Mỗi Đại Vận có một Cung Vận riêng chứa các sao đại diện cho giai đoạn đó.

Tiểu Vận là giai đoạn vận ngắn hơn, thường là 1 năm, cho biết chi tiết về từng năm cụ thể. Tiểu Vận cung cấp thông tin chi tiết hơn về cơ hội và thách thức trong từng năm. Khi phân tích Vận, cần xem xét cả Đại Vận và Tiểu Vận: Đại Vận cho xu hướng lớn, Tiểu Vận cho chi tiết cụ thể. Trong hệ thống, Vận được implement như complex data structures với timeline và các sao tương ứng.

### 15. Tứ Hóa Lưu Niên (四化流年 - Yearly Transformations)

Tứ Hóa Lưu Niên là bốn sao Hóa được tính cho từng năm cụ thể, mang ý nghĩa về những biến đổi trong năm đó. Khác với Tứ Hóa cố định trong lá số, Tứ Hóa Lưu Niên thay đổi mỗi năm dựa trên năm dương lịch. Việc xác định Tứ Hóa Lưu Niên giúp dự đoán những sự kiện và biến đổi quan trọng trong từng năm.

Năm Dần thường mang Hóa Lộc, năm Mão mang Hóa Quyền, năm Thìn mang Hóa Khoa, năm Tỵ mang Hóa Lưu, và chu kỳ tiếp tục. Tứ Hóa Lưu Niên được đặt vào các cung dựa trên cung Mệnh và các quy tắc riêng. Khi phân tích năm, cần xem xét Tứ Hóa Lưu Niên cùng với các sao khác trong cung Vận Niên để có bức tranh đầy đủ về vận năm đó.

### 16. Thập Bát Hạ (十八殺 - Eighteen Harmful Combinations)

Thập Bát Hạ là nhóm 18 cặp tổ hợp xấu trong Tử Vi, mỗi cặp mang một ý nghĩa xấu khác nhau. Các cặp này được tạo thành từ sự kết hợp của các sao và các cung, mang năng lượng xung đột và gây ra những vấn đề trong cuộc sống. Khi một cặp Thập Bát Hạ xuất hiện trong lá số hoặc trong Vận, người đọc số cần lưu ý và đưa ra lời khuyên phù hợp.

Một số cặp Thập Bát Hạ phổ biến bao gồm: Xung Phá (xuất hiện khi các sao xấu xung nhau), Không Nhất (xuất hiện khi cung không có sao hoặc chỉ có sao xấu), và các cặp khác liên quan đến sức khỏe, tài chính, và mối quan hệ. Việc nhận diện Thập Bát Hạ giúp xác định những giai đoạn khó khăn và đề xuất cách ứng phó.

### 17. Xung (冲 - Clash/Opposition)

Xung là mối quan hệ xung đột giữa hai cung đối diện nhau trong vòng tròn 12 cung, mang năng lượng căng thẳng và đối đầu. Khi một cung có sao xấu, cung đối diện (cung Xung) thường bị ảnh hưởng tiêu cực. Xung có nhiều mức độ: Xung nhẹ, Xung nặng, và Đại Xung, tùy thuộc vào các sao trong cung và vị trí của Tử Vi.

Xung không phải lúc nào cũng xấu; trong một số trường hợp, Xung có thể mang lại động lực thay đổi và phát triển. Tuy nhiên, khi Xung xuất hiện trong Vận, nó thường báo hiệu những thách thức và biến cố cần vượt qua. Trong phân tích, Xung cần được xem xét cùng với Liên Cung và các sao trong cung để đưa ra đánh giá toàn diện.

### 18. Hợp (合 - Harmony/Combination)

Hợp là mối quan hệ hài hòa giữa các cung trong Tử Vi, mang năng lượng hỗ trợ và bổ trợ lẫn nhau. Có nhiều loại Hợp: Tam Hợp (ba cung hợp nhau theo nhóm), Song Hợp (hai cung hợp nhau), và Tứ Hợp (bốn cung hợp nhau). Khi các cung Hợp có sao tốt, chúng tạo ra năng lượng thuận lợi và hỗ trợ lẫn nhau.

Tam Hợp cơ bản bao gồm: Mệnh-Thiên Di-Tài Bạch (Tam Hợp Phúc Di), Phụ Mẫu-Huynh Đệ-Nô Bộc (Tam Hợp Phụ Bồi), Tướng Phú-Phu Thê-Tử Tức (Tam Hợp Quan Tử), và Điền Trạch-Phúc Đức (Tam Hợp Điền Phúc). Khi một cung trong Tam Hợp có sao tốt, các cung còn lại cũng được hưởng lợi. Ngược lại, khi một cung có sao xấu, các cung Hợp có thể bị ảnh hưởng.

## Kết luận

Từ điển thuật ngữ này cung cấp nền tảng kiến thức vững chắc về các khái niệm trong Tử Vi Đẩu Số. Việc hiểu rõ từng thuật ngữ và mối quan hệ giữa chúng là điều kiện tiên quyết để xây dựng hệ thống Tử Vi chính xác và có giá trị. Các developers nên tham khảo các tài liệu chuyên sâu và hợp tác với các chuyên gia Tử Vi để đảm bảo độ chính xác trong implementation.
